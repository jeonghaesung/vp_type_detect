#  Copyright (c) 2024, RTE (https://www.rte-france.com)
#  See AUTHORS.txt
#  SPDX-License-Identifier: MPL-2.0
#  This file is part of BERTrend.
import streamlit as st
from urllib.parse import urlparse

from bertrend.demos.demos_utils.i18n import translate
from bertrend.demos.demos_utils.icons import SUCCESS_ICON
from bertrend.demos.demos_utils.state_utils import SessionStateManager
from bertrend.services.embedding_service import EmbeddingService
from bertrend.utils.data_loading import TEXT_COLUMN


def display_embed_documents_component():
    """
    Common Streamlit UI component for embedding documents.
    """
    # Embed documents
    if st.button(translate("embed_documents")):
        with st.spinner(translate("embedding_documents")):
            embedding_dtype = SessionStateManager.get("embedding_dtype")
            embedding_model_name = SessionStateManager.get("embedding_model_name")
            if SessionStateManager.get("embedding_service_type", "remote") == "local":
                embedding_service = EmbeddingService(
                    local=True,
                    model_name=embedding_model_name,
                    embedding_dtype=embedding_dtype,
                )
            else:
                embedding_service_url = SessionStateManager.get("embedding_service_url")
                parsed_url = urlparse(embedding_service_url or "")
                if not (parsed_url.scheme and parsed_url.netloc):
                    raise ValueError(
                        translate("invalid_remote_embedding_url").format(
                            url=embedding_service_url
                        )
                    )
                embedding_service = EmbeddingService(
                    local=False,
                    url=embedding_service_url,
                )
                SessionStateManager.set(
                    "embedding_model_name", embedding_service.embedding_model_name
                )

            texts = SessionStateManager.get_dataframe("time_filtered_df")[
                TEXT_COLUMN
            ].tolist()

            embeddings, token_strings, token_embeddings = embedding_service.embed(
                texts=texts,
            )

            SessionStateManager.set(
                "embedding_model", embedding_service.embedding_model
            )
            SessionStateManager.set("embeddings", embeddings)
            SessionStateManager.set("token_strings", token_strings)
            SessionStateManager.set("token_embeddings", token_embeddings)

            SessionStateManager.set("data_embedded", True)

            st.success(translate("embeddings_calculated_message"), icon=SUCCESS_ICON)
