# Jump The Queue Application

In this section we are going to explain the project structure and how to configure the project.

## Environment Configuration

You can use Pydantic Settings to handle the settings or configurations for your application, with all the power of Pydantic models. The project uses Dependency Injection for managing dependencies across the application and easy mocking for testing.

**Create an **_.env_** file for each environment configuration**. The use of @lru_cache() lets you avoid reading the dotenv file again and again for each request, while allowing you to override it during testing.

Even when using a dotenv file, the application will still read environment variables as well as the dotenv file, **environment variables will always take priority over values loaded from a dotenv file**.

You can also specify the environment when launching the server. Corresponding **_.env_** file will be automatically loaded.

Settings and environment variables are managed by **Pydantic**, refer to [the documentation](https://pydantic-docs.helpmanual.io/usage/settings/) for more info.

```
ENV=PROD uvicorn main:app --reload
ENV=PROD python main.py
```

### Host & Port Configuration
The Port and Hosting configuration can be set directly on the **.env** file if launching the main.py file.

However, this configuration is related with the uvicorn server itself and can also be set with the _**--port [int]**_ flag. 

Refer to the [uvicorn documentation](https://www.uvicorn.org/settings/) for more info.

### Logging Configuration
The application uses the default **_logging_** module.

To use it inside an specific module init it first with the command:

```
logger = logging.getLogger(__name__)
```

You can use the __name__ variable to take the current file name as the default or specify a custom module name manually.

Configure the logging properties in the **_logging.yaml_** file. 
You can find more information in the [logging](https://docs.python.org/3/library/logging.html#module-logging) documentation.

## Project Structure


