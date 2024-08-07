"""Jac Language Features."""

from collections import OrderedDict
from dataclasses import Field, MISSING, fields
from functools import wraps
from inspect import iscoroutinefunction
from os import getenv
from re import compile
from typing import Any, Callable, Type, TypeVar, cast, get_type_hints

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
)
from fastapi.responses import ORJSONResponse

from jaclang.compiler.absyntree import AstAsyncNode
from jaclang.compiler.constant import EdgeDir
from jaclang.compiler.passes.main.pyast_gen_pass import PyastGenPass
from jaclang.plugin.default import hookimpl
from jaclang.plugin.feature import JacFeature as Jac

from orjson import loads

from pydantic import BaseModel, Field as pyField, ValidationError, create_model

from starlette.datastructures import UploadFile as BaseUploadFile

from ..core.architype import (
    Anchor,
    Architype,
    DSFunc,
    EdgeArchitype,
    GenericEdge,
    NodeAnchor,
    NodeArchitype,
    Root,
    WalkerAnchor,
    WalkerArchitype,
)
from ..core.context import JaseciContext
from ..jaseci.security import authenticator


T = TypeVar("T")
DISABLE_AUTO_ENDPOINT = getenv("DISABLE_AUTO_ENDPOINT") == "true"
PATH_VARIABLE_REGEX = compile(r"{([^\}]+)}")
FILE_TYPES = {
    UploadFile,
    list[UploadFile],
    UploadFile | None,
    list[UploadFile] | None,
}

walker_router = APIRouter(prefix="/walker", tags=["walker"])


def get_specs(cls: type) -> Type["DefaultSpecs"] | None:
    """Get Specs and inherit from DefaultSpecs."""
    specs = getattr(cls, "__specs__", None)
    if specs is None:
        if DISABLE_AUTO_ENDPOINT:
            return None
        specs = DefaultSpecs

    if not issubclass(specs, DefaultSpecs):
        specs = type(specs.__name__, (specs, DefaultSpecs), {})

    return specs


def gen_model_field(cls: type, field: Field, is_file: bool = False) -> tuple[type, Any]:
    """Generate Specs for Model Field."""
    if field.default is not MISSING:
        consts = (cls, pyField(default=field.default))
    elif callable(field.default_factory):
        consts = (cls, pyField(default_factory=field.default_factory))
    else:
        consts = (cls, File(...) if is_file else ...)

    return consts


def populate_apis(cls: Type[WalkerArchitype]) -> None:
    """Generate FastAPI endpoint based on WalkerArchitype class."""
    if (specs := get_specs(cls)) and not specs.private:
        path: str = specs.path or ""
        methods: list = specs.methods or []
        as_query: str | list = specs.as_query or []
        auth: bool = specs.auth or False

        query: dict[str, Any] = {}
        body: dict[str, Any] = {}
        files: dict[str, Any] = {}

        if path:
            if not path.startswith("/"):
                path = f"/{path}"
            if isinstance(as_query, list):
                as_query += PATH_VARIABLE_REGEX.findall(path)

        hintings = get_type_hints(cls)
        for f in fields(cls):
            f_name = f.name
            f_type = hintings[f_name]
            if f_type in FILE_TYPES:
                files[f_name] = gen_model_field(f_type, f, True)
            else:
                consts = gen_model_field(f_type, f)

                if as_query == "*" or f_name in as_query:
                    query[f_name] = consts
                else:
                    body[f_name] = consts

        payload: dict[str, Any] = {
            "query": (
                create_model(f"{cls.__name__.lower()}_query_model", **query),
                Depends(),
            ),
            "files": (
                create_model(f"{cls.__name__.lower()}_files_model", **files),
                Depends(),
            ),
        }

        body_model = None
        if body:
            body_model = create_model(f"{cls.__name__.lower()}_body_model", **body)

            if files:
                payload["body"] = (UploadFile, File(...))
            else:
                payload["body"] = (body_model, ...)

        payload_model = create_model(f"{cls.__name__.lower()}_request_model", **payload)

        async def api_entry(
            request: Request,
            node: str | None,
            payload: payload_model = Depends(),  # type: ignore # noqa: B008
        ) -> ORJSONResponse:
            pl = cast(BaseModel, payload).model_dump()
            body = pl.get("body", {})

            if isinstance(body, BaseUploadFile) and body_model:
                body = loads(await body.read())
                try:
                    body = body_model(**body).model_dump()
                except ValidationError as e:
                    return ORJSONResponse({"detail": e.errors()})

            jctx = await JaseciContext.create(request, NodeAnchor.ref(node or ""))

            wlk: WalkerAnchor = cls(**body, **pl["query"], **pl["files"]).__jac__
            if await jctx.validate_access():
                await wlk.spawn_call(jctx.entry)
                await jctx.close()
                return ORJSONResponse(jctx.response(wlk.returns))
            else:
                await jctx.close()
                raise HTTPException(
                    403,
                    f"You don't have access on target entry{cast(Anchor, jctx.entry).ref_id}!",
                )

        async def api_root(
            request: Request,
            payload: payload_model = Depends(),  # type: ignore # noqa: B008
        ) -> Response:
            return await api_entry(request, None, payload)

        for method in methods:
            method = method.lower()

            walker_method = getattr(walker_router, method)

            settings: dict[str, list[Any]] = {"tags": ["walker"]}
            if auth:
                settings["dependencies"] = cast(list, authenticator)

            walker_method(url := f"/{cls.__name__}{path}", summary=url, **settings)(
                api_root
            )
            walker_method(
                url := f"/{cls.__name__}/{{node}}{path}", summary=url, **settings
            )(api_entry)


def specs(
    cls: Type[WalkerArchitype] | None = None,
    *,
    path: str = "",
    methods: list[str] = ["post"],  # noqa: B006
    as_query: str | list = [],  # noqa: B006
    auth: bool = True,
    private: bool = False,
) -> Callable:
    """Walker Decorator."""

    def wrapper(cls: Type[WalkerArchitype]) -> Type[WalkerArchitype]:
        if get_specs(cls) is None:
            p = path
            m = methods
            aq = as_query
            a = auth
            pv = private

            class __specs__(DefaultSpecs):  # noqa: N801
                path: str = p
                methods: list[str] = m
                as_query: str | list = aq
                auth: bool = a
                private: bool = pv

            cls.__specs__ = __specs__  # type: ignore[attr-defined]

            populate_apis(cls)
        return cls

    if cls:
        return wrapper(cls)

    return wrapper


class DefaultSpecs:
    """Default API specs."""

    path: str = ""
    methods: list[str] = ["post"]
    as_query: str | list[str] = []
    auth: bool = True
    private: bool = False


class JacPlugin:
    """Jaseci Implementations."""

    @staticmethod
    @hookimpl
    def context() -> JaseciContext:
        """Get the execution context."""
        return JaseciContext.get()

    @staticmethod
    @hookimpl
    def make_architype(
        cls: type,
        arch_base: Type[Architype],
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a new architype."""
        for i in on_entry + on_exit:
            i.resolve(cls)
        if not hasattr(cls, "_jac_entry_funcs_") or not hasattr(
            cls, "_jac_exit_funcs_"
        ):
            # Saving the module path and reassign it after creating cls
            # So the jac modules are part of the correct module
            cur_module = cls.__module__
            cls = type(cls.__name__, (cls, arch_base), {})
            cls.__module__ = cur_module
            cls._jac_entry_funcs_ = on_entry  # type: ignore
            cls._jac_exit_funcs_ = on_exit  # type: ignore
        else:
            new_entry_funcs = OrderedDict(zip([i.name for i in on_entry], on_entry))
            entry_funcs = OrderedDict(
                zip([i.name for i in cls._jac_entry_funcs_], cls._jac_entry_funcs_)
            )
            entry_funcs.update(new_entry_funcs)
            cls._jac_entry_funcs_ = list(entry_funcs.values())

            new_exit_funcs = OrderedDict(zip([i.name for i in on_exit], on_exit))
            exit_funcs = OrderedDict(
                zip([i.name for i in cls._jac_exit_funcs_], cls._jac_exit_funcs_)
            )
            exit_funcs.update(new_exit_funcs)
            cls._jac_exit_funcs_ = list(exit_funcs.values())

        inner_init = cls.__init__  # type: ignore

        @wraps(inner_init)
        def new_init(
            self: Architype,
            *args: object,
            __jac__: Anchor | None = None,
            **kwargs: object,
        ) -> None:
            arch_base.__init__(self, __jac__)
            inner_init(self, *args, **kwargs)

        cls.__init__ = new_init  # type: ignore
        return cls

    @staticmethod
    @hookimpl
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacPlugin.make_architype(
                cls=cls, arch_base=Architype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacPlugin.make_architype(
                cls=cls, arch_base=NodeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacPlugin.make_architype(
                cls=cls, arch_base=EdgeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a walker architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacPlugin.make_architype(
                cls=cls, arch_base=WalkerArchitype, on_entry=on_entry, on_exit=on_exit
            )
            populate_apis(cls)
            return cls

        return decorator

    @staticmethod
    @hookimpl
    async def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Jac's spawn operator feature."""
        if isinstance(op1, WalkerArchitype):
            return await op1.__jac__.spawn_call(op2.__jac__)
        elif isinstance(op2, WalkerArchitype):
            return await op2.__jac__.spawn_call(op1.__jac__)
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""
        JaseciContext.get().reports.append(expr)

    @staticmethod
    @hookimpl
    async def ignore(
        walker: WalkerArchitype,
        expr: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
    ) -> bool:
        """Jac's ignore stmt feature."""
        if isinstance(walker, WalkerArchitype):
            return await walker.__jac__.ignore_node(
                (i.__jac__ for i in expr) if isinstance(expr, list) else [expr.__jac__]
            )
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    async def visit_node(
        walker: WalkerArchitype,
        expr: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
    ) -> bool:
        """Jac's visit stmt feature."""
        if isinstance(walker, WalkerArchitype):
            return await walker.__jac__.visit_node(
                (i.__jac__ for i in expr) if isinstance(expr, list) else [expr.__jac__]
            )
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    async def edge_ref(
        node_obj: NodeArchitype | list[NodeArchitype],
        target_cls: Type[NodeArchitype] | list[Type[NodeArchitype]] | None,
        dir: EdgeDir,
        filter_func: Callable[[list[EdgeArchitype]], list[EdgeArchitype]] | None,
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's apply_dir stmt feature."""
        if isinstance(node_obj, NodeArchitype):
            node_obj = [node_obj]
        targ_cls_set: list[Type[NodeArchitype]] | None = (
            [target_cls] if isinstance(target_cls, type) else target_cls
        )
        if edges_only:
            connected_edges: list[EdgeArchitype] = []
            for node in node_obj:
                connected_edges += await node.__jac__.get_edges(
                    dir, filter_func, target_cls=targ_cls_set
                )
            return list(set(connected_edges))
        else:
            connected_nodes: list[NodeArchitype] = []
            for node in node_obj:
                connected_nodes.extend(
                    await node.__jac__.edges_to_nodes(
                        dir, filter_func, target_cls=targ_cls_set
                    )
                )
            return list(set(connected_nodes))

    @staticmethod
    @hookimpl
    async def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge_spec: Callable[[], EdgeArchitype],
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        left = [left] if isinstance(left, NodeArchitype) else left
        right = [right] if isinstance(right, NodeArchitype) else right
        edges = []
        nodes = []
        for i in left:
            for j in right:
                if await (source := i.__jac__).has_connect_access(target := j.__jac__):
                    conn_edge = edge_spec()
                    edges.append(conn_edge)
                    nodes.append(j)
                    source.connect_node(target, conn_edge.__jac__)
        return nodes if not edges_only else edges

    @staticmethod
    @hookimpl
    async def disconnect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        dir: EdgeDir,
        filter_func: Callable[[list[EdgeArchitype]], list[EdgeArchitype]] | None,
    ) -> bool:  # noqa: ANN401
        """Jac's disconnect operator feature."""
        disconnect_occurred = False
        left = [left] if isinstance(left, NodeArchitype) else left
        right = [right] if isinstance(right, NodeArchitype) else right
        for i in left:
            node = i.__jac__
            for anchor in set(node.edges):
                if (
                    (architype := await anchor.sync(node))
                    and (source := anchor.source)
                    and (target := anchor.target)
                    and (not filter_func or filter_func([architype]))
                    and (src_arch := await source.sync())
                    and (trg_arch := await target.sync())
                ):
                    if (
                        dir in [EdgeDir.OUT, EdgeDir.ANY]
                        and node == source
                        and trg_arch in right
                        and await source.has_write_access(target)
                    ):
                        anchor.destroy()
                        disconnect_occurred = True
                    if (
                        dir in [EdgeDir.IN, EdgeDir.ANY]
                        and node == target
                        and src_arch in right
                        and await target.has_write_access(source)
                    ):
                        anchor.destroy()
                        disconnect_occurred = True

        return disconnect_occurred

    @staticmethod
    @hookimpl
    async def get_root() -> Root:
        """Jac's assign comprehension feature."""
        if architype := await JaseciContext.get().root.sync():
            return cast(Root, architype)
        raise Exception("No Available Root!")

    @staticmethod
    @hookimpl
    def get_root_type() -> Type[Root]:
        """Jac's root getter."""
        return Root

    @staticmethod
    @hookimpl
    def build_edge(
        is_undirected: bool,
        conn_type: Type[EdgeArchitype] | EdgeArchitype | None,
        conn_assign: tuple[tuple, tuple] | None,
    ) -> Callable[[], EdgeArchitype]:
        """Jac's root getter."""
        conn_type = conn_type if conn_type else GenericEdge

        def builder() -> EdgeArchitype:
            edge = conn_type() if isinstance(conn_type, type) else conn_type
            edge.__jac__.is_undirected = is_undirected
            if conn_assign:
                for fld, val in zip(conn_assign[0], conn_assign[1]):
                    if hasattr(edge, fld):
                        setattr(edge, fld, val)
                    else:
                        raise ValueError(f"Invalid attribute: {fld}")
            return edge

        return builder


##########################################################
#               NEED TO TRANSFER TO PLUGIN               #
##########################################################

Jac.RootType = Root  # type: ignore[assignment]
Jac.Obj = Architype  # type: ignore[assignment]
Jac.Node = NodeArchitype  # type: ignore[assignment]
Jac.Edge = EdgeArchitype  # type: ignore[assignment]
Jac.Walker = WalkerArchitype  # type: ignore[assignment]


def overrided_init(self: AstAsyncNode, is_async: bool) -> None:
    """Initialize ast."""
    self.is_async = True


AstAsyncNode.__init__ = overrided_init  # type: ignore[method-assign]
PyastGenPass.set(
    [
        name
        for name, func in JacPlugin.__dict__.items()
        if isinstance(func, staticmethod) and iscoroutinefunction(func.__func__)
    ]
)
