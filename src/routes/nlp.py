from fastapi import APIRouter, FastAPI, status, Request
from fastapi.responses import JSONResponse
import logging

from controllers.nlp_controller import NLPController
from models.chunk_model import ChunkModel
from models.project_model import ProjectModel
from routes.schema.nlp_schema import IndexPushRequestSchema, SearchRequestSchema

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["nlp"],
)


@nlp_router.post("/index/push/{project_id}")
async def index_project(
    request: Request, project_id: str, push_request: IndexPushRequestSchema
):

    project_model = await ProjectModel.create_instance(request.app.state.db_client)
    project = await project_model.get_project(project_id)

    if project is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Project not found"},
        )

    nlp_controller = NLPController(
        vector_db_client=request.app.state.vector_db_client,
        generation_client=request.app.state.genration_client,
        embedding_client=request.app.state.embedding_client,
        template_parser=request.app.state.template_parser,
    )

    chunk_model = await ChunkModel.create_instance(request.app.state.db_client)

    has_records = True
    page = 1
    idx = 0

    while has_records:
        page_chunks = await chunk_model.get_chunck(
            chunk_project_id=project.project_id, page=page
        )

        if len(page_chunks[0]) == 0 or not page_chunks[0]:
            has_records = False
            break
        else:
            page += 1

        chunks_ids = list(range(idx, idx + len(page_chunks[0])))
        idx += len(page_chunks[0])

        res = nlp_controller.index_into_vector_db(
            project_id=project.project_id,
            chunks=page_chunks[0],
            chunks_ids=chunks_ids,
            reset=push_request.reset,
        )

        if res is False:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Indexing failed"},
            )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Indexing completed"},
    )


@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str):

    project_model = await ProjectModel.create_instance(request.app.state.db_client)
    project = await project_model.get_project(project_id)

    if project is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Project not found"},
        )

    nlp_controller = NLPController(
        vector_db_client=request.app.state.vector_db_client,
        generation_client=request.app.state.genration_client,
        embedding_client=request.app.state.embedding_client,
        template_parser=request.app.state.template_parser,
    )

    return nlp_controller.get_vector_db_collection_info(project.project_id)


@nlp_router.post("/index/search/{project_id}")
async def search_project_db_collection(
    request: Request, project_id: str, search_request: SearchRequestSchema
):

    project_model = await ProjectModel.create_instance(request.app.state.db_client)
    project = await project_model.get_project(project_id)

    if project is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Project not found"},
        )

    nlp_controller = NLPController(
        vector_db_client=request.app.state.vector_db_client,
        generation_client=request.app.state.genration_client,
        embedding_client=request.app.state.embedding_client,
        template_parser=request.app.state.template_parser,
    )

    return nlp_controller.search_project_db_collection(
        project.project_id,
        text=search_request.text,
        limit=search_request.limit,
        offset=search_request.offset,
    )


@nlp_router.post("/index/answer/{project_id}")
async def answer_rag_question(
    request: Request, project_id: str, search_request: SearchRequestSchema
):

    project_model = await ProjectModel.create_instance(request.app.state.db_client)
    project = await project_model.get_project(project_id)

    if project is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Project not found"},
        )

    nlp_controller = NLPController(
        vector_db_client=request.app.state.vector_db_client,
        generation_client=request.app.state.genration_client,
        embedding_client=request.app.state.embedding_client,
        template_parser=request.app.state.template_parser,
    )

    answer, full_prompt, chat_hitory = nlp_controller.answer_rag_question(
        project=project,
        text=search_request.text,
        limit=search_request.limit,
        offset=search_request.offset,
    )
    if answer is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Answer not found"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_hitory": chat_hitory,
        },
    )
