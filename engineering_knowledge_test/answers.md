# Engineering Knowledge AI Agent Test

## 1. Describe differences between REST API, MCP in the context of AI.

REST API are stateless HTTP reqeusts. For each REST API request it needs its own authentication and parameters. They allow a system to access another systems function or data if used for a traditional software like a web app it scales well for millions of request at a time. But in the use for AI, the AI must send different REST APIs if they want to access multiple different tools. The AI must know in advance which endpoint to use, there is no way to decide something in the middle of the conversation.

MCP (Model Context Protocol) is an open source tool that enable AI systems to connect to external systems in a standardized way. When using a MCP an AI can connect to data sources (databases, local files), tools (web search, specific functions) and even workflows since it will use the same protocol. After connecting to a MCP server the ai can dynamicly see tools that are available in real time.

MCP servers are best used in cases where multiple integrations are needed, dynamic tool changes or AI orchestration. REST APIs has their uses cases aswell, for example if we only need a single purpose automation script. It will be much simpler if to do a single API call especially if low latency and high throuput is a priority.

## 2. How REST API, MCP, can improve the AI use case.

REST API improves AI use case by giving access to traditional information like databases or microservices. By using existing APIs we could give AI a determenistic way to do tasks in a proven and scalable way (like writing an email or getting order data).

MCP multiplies the AI by having an abstract integration layer. Since we don't need a custom logic for each tool, a developer can just deploy a MCP server that an AI Agent can immediately understand and use. This makes a very autonomous AI use case since it could see all available tools nad just pick the correct one to use and execute multistep reasoning.

## 3. How do you ensure that your AI agent answers correctly?

1. RAG (Retrieval Augmented Generation), we can reduce hallucinations by giving the AI grounded information from databases or documents. WE could implement a hybrid retrieval system (vector & keyword) and reranking to make sure the information retrieved is as relevant & accurate as possible
2. Structured Output, we make the AI agent answer in a structured and consistent way every time (example answer, reasoning, citations). We also can implement a strict rule on if there is no source of truth we do not output an answer.
3. Evaluations, track metrics (faithfullness, relevance, precision & recall) and use LLM as a judge to score on these metrics
4. Input/output Moderation, deploy sentiment classifier or rule based filters to block prompt injections as inputs and or filtering out non compliant outputs

## 4. Describe what can you do with Docker / Containerize environment in the context of AI

1. Reproducable environments, AI models rely on dertain system dependencies. Using docker and containerizing them makes the model run on local or production server.
2. Microservices, we can break down complex AI systems into different microservices like embedding model, LLM, MCP servers, etc. into seperate containers. Each of them can be scaled seperately as needed
3. Code Sandbox, if we are giving the AI a tool to run code, Docker can provide a secure sandbox or virtual machine. In this sandbox the AI can test and run the generated code without any risks involving production code, databases or other internal systems.

## 5. How do you finetune the LLM model from raw ?

Steps in finetuning:

1. Data Preperation: Collect, clean, and annotate data that will be used for finetuning. The quality of the dataset will directly impact the result of the finetuned model. In the data preperation stage data augmentaion, transformation, or deduplication maybe needed. Spiliting this data into training, validation and test sets (usually 80:10:10 split) is also a must since we would need to see if the models output are as expected as we intend to from the begining.
2. Model Initialization: Here you need to select a base LLM model you wwant to fine tune. When choosing a model factors like model size, architecture & base capabilities are what it mostly you need to consider.
3. Training Setup:This step involve setting up necessary hardware and software needed for our finetuning process. If trained locally we would need sufficient GPUs and RAM for our model size or we could also use a cloud machine to handle the hardware requirements. For software installing dependencies like pytorch, tensorflow or other machine learning libraries and making sure these software are compatible.
4. Finetuning: There is 2 main ways to finetune. First is a Full Finetuning where all of the base models parameters are updated, this is very resource heavy but may result in the best performance to our goal. Another way is Partial Finetuning (PEFT) where only a subset of the parameter are updated or adding new smaller layers to the LLM. This way is much more efficient and having lower risk of catastrophice forgetting. Some examples are LoRA and QLoRA.
5. Evaluation:After training is done the model needs to be tested with data it's never seen before (validation and test sets we previously split). This is to make sure the finetuned model generalize well and meet our goal. We can measure metrics like precision, recall, BLEU or even human evaluation.
