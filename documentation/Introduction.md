
# Jump the Queue

The application was built using [Devon4Py](https://github.com/devonfw-forge/devon4py), a 
template implemented by Capgemini that defines how we develop software applications with FastApi.


## Purpose

Customers value their time as much as business owners do, many users are tired of losing their 
order in a queue to be served or not be attended to by not being careful when it arrives theirs 
turns, for example in a store or in a public office because the queue is managed with the classic 
system consisting of a ticket dispenser.

In addition to the waste of paper rolls that cost to generate the tickets that then are throw into the bin.

Capgemini provide a new intelligent management system of shifts in a queue through the generation 
of tickets in a digital way and tracking of the state of the queue at every moment sending notices 
to the client in proper change of state in the queue.

This application helps you to improve the customer’s satisfaction as it eliminates the need to wait 
standing, reduces the actual and perceived wait time and improves your business image.

Capgemini only delivers user-centric and scalable applications which are easy to use and solve your 
problems at the same time.

## Devon4Py Technology Stack

#### Based on FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

The key features are:

- **Fast**: Very high performance, **on par with NodeJS and Go** (thanks to _Starlette_ and _Pydantic_). One of the fastest Python frameworks available.

- **Fast to code**: Increase the speed to develop features by about 200% to 300%.

- **Fewer bugs**: Reduce about 40% of human (developer) induced errors.

- **Intuitive**: Great editor support. Completion everywhere. Less time debugging.

- **Easy**: Designed to be easy to use and learn. Less time reading docs.

- **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.

- **Robust**: Get production-ready code. With automatic interactive documentation.

- **Standards-based**: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema.

FastAPI works on **_Uvicorn_**, an ASGI web server implementation for Python.

Unlike Flask, FastAPI is an ASGI (Asynchronous Server Gateway Interface) framework, brings together Starlette, Pydantic, OpenAPI, and JSON Schema.
Under the hood, FastAPI uses Pydantic for data validation and Starlette for tooling, making it blazing fast compared to Flask, giving comparable performance to high-speed web APIs in Node or Go.
Starlette + Uvicorn offers async request capability, something that Flask lacks.
With Pydantic along with type hints, you get a nice editor experience with autocompletion. You also get data validation, serialization and deserialization (for building an API), and automatic documentation (via JSON Schema and OpenAPI).


### Unlimited "plug-ins"
Or in other way, no need for them, import and use the code you need.

Any integration is designed to be so simple to use (with dependencies) that you can create a "plug-in" for your application in 2 lines of code using the same structure and syntax used for your path operations.

### Tested
- 100% test coverage.
- 100% type annotated code base.
- Used in production applications.

### Based on Starlette

FastAPI is fully compatible with (and based on) [Starlette](https://www.starlette.io/). So, any additional Starlette code you have, will also work.

FastAPI is actually a sub-class of Starlette. So, if you already know or use Starlette, most of the functionality will work the same way.

With FastAPI you get all of Starlette's features (as FastAPI is just Starlette on steroids):

- Seriously impressive performance. It is one of the fastest Python frameworks available, on par with NodeJS and Go.
- WebSocket support.
- In-process background tasks.
- Startup and shutdown events.
- Test client built on requests.
- CORS, GZip, Static Files, Streaming responses.
- Session and Cookie support.
- 100% test coverage.
- 100% type annotated codebase.



