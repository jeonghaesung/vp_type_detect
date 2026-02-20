#  Copyright (c) 2024, RTE (https://www.rte-france.com)
#  See AUTHORS.txt
#  SPDX-License-Identifier: MPL-2.0
#  This file is part of BERTrend.

# Translation dictionaries for demos_utils
TRANSLATIONS = {
    "ctrl_enter": {
        "fr": "CTRL + Entrée pour mettre à jour",
        "en": "CTRL + Enter to update",
        "ko": "CTRL + Enter로 업데이트",
    },
    "select_language": {"fr": "Choisir une langue", "en": "Select Language", "ko": "언어 선택"},
    "embedding_model": {"fr": "Modèle d'embedding", "en": "Embedding Model", "ko": "임베딩 모델"},
    "embedding_service_url": {
        "fr": "URL du service d'embedding",
        "en": "Embedding service URL",
    },
    "embedding_hyperparameters": {
        "fr": "Paramètres d'embedding",
        "en": "Embedding settings",
        "ko": "임베딩 설정",
    },
    "embedding_service": {
        "fr": "Service d'embedding",
        "en": "Embedding Service",
    },
    "bertopic_hyperparameters": {
        "fr": "Hyperparamètres BERTopic",
        "en": "BERTopic Hyperparameters",
    },
    "bertrend_hyperparameters": {
        "fr": "Hyperparamètres BERTrend",
        "en": "BERTrend Hyperparameters",
    },
    "embeddings_calculated_message": {
        "fr": "Embeddings calculés avec succès !",
        "en": "Embeddings calculated successfully!",
    },
    "no_embeddings_warning_message": {
        "fr": "Veuillez vectoriser les données et entraîner les modèles avant de procéder à l'analyse.",
        "en": "Please embed data and train models before proceeding to analysis.",
    },
    "model_training_complete_message": {
        "fr": "Entraînement du modèle terminé !",
        "en": "Model training complete!",
    },
    "no_data_after_preprocessing_message": {
        "fr": "Aucune donnée disponible après prétraitement. Veuillez vérifier les fichiers sélectionnés et les options de prétraitement.",
        "en": "No data available after preprocessing. Please check the selected files and preprocessing options.",
    },
    "select_from_local_storage": {
        "fr": "Selection de jeux de données à partir du stockage local (.xlsx, .csv, .json, .jsonl, .parquet)",
        "en": "Select dataset from local storage (.xlsx, .csv, .json, .jsonl, .parquet)",
        "ko": "로컬 저장소에서 데이터셋 선택 (.xlsx, .csv, .json, .jsonl, .parquet)",
    },
    "select_from_remote_storage": {
        "fr": "Selection de jeux de données sur le serveur",
        "en": "Select one or more datasets from the server data",
        "ko": "서버 데이터에서 하나 이상의 데이터셋 선택",
    },
    "data_loading": {
        "fr": "Chargement des données",
        "en": "Data loading",
        "ko": "데이터 로딩",
    },
    "local_data": {
        "fr": "Données locales",
        "en": "Data from local storage",
        "ko": "로컬 데이터",
    },
    "remote_data": {"fr": "Données sur le serveur", "en": "Data from server", "ko": "서버 데이터"},
    "data_filtering": {"fr": "Filtrage des données", "en": "Data filtering", "ko": "데이터 필터링"},
    "embed_documents": {
        "fr": "Vectoriser les documents",
        "en": "Embed Documents",
    },
    "embedding_documents": {
        "fr": "Vectorisation des documents...",
        "en": "Embedding documents...",
    },
    "no_dataset_warning": {
        "fr": "Veuillez sélectionner au moins un jeu de données pour continuer.",
        "en": "Please select at least one dataset to proceed.",
        "ko": "계속하려면 최소 1개의 데이터셋을 선택하세요.",
    },
    "error_loading_file": {
        "fr": "Erreur lors du chargement du fichier '{file_name}': {error}",
        "en": "Error while loading file '{file_name}': {error}",
    },
    "drag_drop_help": {
        "fr": "Glissez et déposez les fichiers à utiliser comme jeu de données dans cette zone",
        "en": "Drag and drop files to be used as dataset in this area",
    },
    "raw_documents_count": {
        "fr": "Nombre de documents dans les données brutes: **{count}**",
        "en": "Number of documents in raw data: **{count}**",
        "ko": "원본 데이터 문서 수: **{count}**",
    },
    "minimum_characters": {
        "fr": "Nombre minimum de caractères",
        "en": "Minimum Characters",
    },
    "minimum_characters_help": {
        "fr": "Nombre minimum de caractères que chaque document doit contenir.",
        "en": "Minimum number of characters each document must contain.",
    },
    "sample_ratio": {
        "fr": "Ratio d'échantillonnage",
        "en": "Sample ratio",
    },
    "sample_ratio_help": {
        "fr": "Fraction des données brutes à utiliser pour calculer les sujets. Échantillonne aléatoirement les documents à partir des données brutes.",
        "en": "Fraction of raw data to use for computing topics. Randomly samples documents from raw data.",
    },
    "split_by_paragraphs": {
        "fr": "Diviser le texte par paragraphes",
        "en": "Split text by paragraphs",
    },
    "split_option_yes": {
        "fr": "oui",
        "en": "yes",
    },
    "split_option_no": {
        "fr": "non",
        "en": "no",
    },
    "split_option_enhanced": {
        "fr": "amélioré",
        "en": "enhanced",
    },
    "split_help": {
        "fr": "'Pas de division': Pas de division sur les documents ; 'Division par paragraphes': Divise les documents en paragraphes ; 'Division améliorée': utilise une méthode plus avancée mais plus lente pour la division qui prend en compte la longueur d'entrée maximale du modèle d'embedding.",
        "en": "'No split': No splitting on the documents ; 'Split by paragraphs': Split documents into paragraphs ; 'Enhanced split': uses a more advanced but slower method for splitting that considers the embedding model's maximum input length.",
    },
    "select_timeframe": {
        "fr": "Sélectionner la période",
        "en": "Select Timeframe",
    },
    "filtered_documents_count": {
        "fr": "Nombre de documents dans les données filtrées: **{count}**",
        "en": "Number of documents in filtered data: **{count}**",
        "ko": "필터링 후 문서 수: **{count}**",
    },
    "settings_and_controls": {
        "fr": "Paramètres et contrôles",
        "en": "Settings and Controls",
        "ko": "설정 및 제어",
    },
    "column_selection": {
        "fr": "Sélection des colonnes",
        "en": "Column Selection",
    },
    "text_column_selection": {
        "fr": "Sélection de la colonne contenant le texte",
        "en": "Select Column Containing Text",
    },
    "timestamp_column_selection": {
        "fr": "Sélection de la colonne contenant l'horodatage",
        "en": "Select Column Containing Timestamp",
    },
    "invalid_remote_embedding_url": {
        "fr": "URL invalide pour le service d'embedding distant: '{url}'. Veuillez saisir une URL complète (ex: http://localhost:8000) ou sélectionner le mode local.",
        "en": "Invalid remote embedding service URL: '{url}'. Please enter a full URL (e.g., http://localhost:8000) or switch to local mode.",
        "ko": "원격 임베딩 서비스 URL이 올바르지 않습니다: '{url}'. 전체 URL(예: http://localhost:8000)을 입력하거나 로컬 모드로 전환하세요.",
    },
    "demo_sample_data_info": {
        "fr": "Exemple inclus: demo_samples/korean_voice_phishing_samples.csv",
        "en": "Bundled sample: demo_samples/korean_voice_phishing_samples.csv",
        "ko": "기본 샘플: demo_samples/korean_voice_phishing_samples.csv",
    },
    "language_selector": {"fr": "Langue", "en": "Language", "ko": "언어"},
}
