# LangGraph SQL Analysis Workflow

A state-based workflow system for processing natural language queries, generating SQL, and creating visualizations using LangGraph and LangChain.

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Start Project

```bash
# Clone the repository
git clone https://github.com/spandan114/LuminAI-Data-Analyst.git
cd lumin_ai

```

### Start Project
```bash
# Start the containers
docker compose up --build
```

### Remove Project

```bash
# Stop and remove containers
docker compose down
```

## Modules & Tools

- Python 3.8+
- LangGraph
- LangChain
- SQL Database (PostgreSQL recommended)

## ⚡ Features

- Natural language query processing
- Automated SQL generation and validation
- Dynamic visualization selection
- Fallback to conversational responses
- State-based workflow management



## 🔄 Workflow Architecture

##### High level flow
```mermaid
flowchart TD
    Start([Start]) --> InputDoc{Document Type?}
    
    %% Document Processing Branch
    InputDoc -->|CSV/Excel| DB[(Database)]
    InputDoc -->|PDF/Text| VEC[(pgvector DB)]
    InputDoc -->|SQL Connection| DBTable[(DB Table)]
    
    %% Data Source Selection
    DB --> DataSelect{Data Source?}
    VEC --> DataSelect
    DBTable --> DataSelect
    
    %% Query Processing
    DataSelect -->|CSV/Excel/DB Link| QueryDB[Query Database]
    DataSelect -->|PDF/Text| QueryVec[Query Vector Database]
    
    QueryDB --> Process[Process Data]
    QueryVec --> Process
    
    %% Question Processing Pipeline
    Process --> Questions[Get User Questions]
    Questions --> ParseQuestions[Parse Questions & Get Relevant Tables/Columns]
    ParseQuestions --> 
    
    %% SQL Validation and Execution
    GenSQL --> ValidateSQL{Validate SQL Query}
    ValidateSQL -->|Need Fix| GenSQL
    ValidateSQL -->|Valid| ExecuteSQL[Execute SQL]
    
    %% Result Processing
    ExecuteSQL --> CheckResult{Check Results}
    CheckResult -->|No Error & Relevant| ChooseViz[Choose Visualization]
    ChooseViz --> FormatViz[Format Data for Visualization]
    CheckResult -->|Error or Not Relevant| FormatResult[Format Result]
    
    %% End States
    FormatViz --> End([End])
    FormatResult --> End
    
    %% Styling
    classDef database fill:#f9f,stroke:#333,stroke-width:2px
    class DB,VEC,DBTable database

```

##### Lang graph flow
The system uses a state-based workflow to process queries and generate appropriate SQL or conversational responses:

```mermaid
flowchart TD
    Start([START]) --> ParseQuestion[Parse Question]
    
    ParseQuestion --> ShouldContinue{Should Continue?}
    
    ShouldContinue -->|Yes| GenSQL[Generate SQL Query]
    GenSQL --> ValidateSQL[Validate and Fix SQL]
    ValidateSQL --> ExecuteSQL[Execute SQL Query]
    
    ExecuteSQL --> FormatResults[Format Results]
    ExecuteSQL --> ChooseViz[Choose Visualization]
    
    ChooseViz --> FormatViz[Format Data for Visualization]
    
    ShouldContinue -->|No| ConvResponse[Conversational Response]
    
    FormatResults --> End([END])
    FormatViz --> End
    ConvResponse --> End
    
    classDef conditional fill:#f9f,stroke:#333,stroke-width:2px
    classDef process fill:#bbf,stroke:#333,stroke-width:1px
    class ShouldContinue conditional
    class ParseQuestion,GenSQL,ValidateSQL,ExecuteSQL,FormatResults,ChooseViz,FormatViz,ConvResponse process
```

## Database Schema 
```mermaid
erDiagram
    users ||--o{ data_sources : creates
    users ||--o{ conversations : has
    data_sources ||--o{ conversations : used_in
    conversations ||--o{ messages : contains

    users {
        int id PK
        string name
        string email UK
        string hashed_password UK
        datetime created_at
    }

    data_sources {
        int id PK
        int user_id FK
        string name
        string type
        string table_name UK
        string connection_url UK
        datetime created_at
    }

    conversations {
        int id PK
        int user_id FK
        int data_source_id FK
        string title
        datetime created_at
        datetime updated_at
    }

    messages {
        int id PK
        int conversation_id FK
        enum role
        json content
        datetime created_at
        datetime updated_at
    }
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
