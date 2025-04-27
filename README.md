# notch

🪓 The Python logging micropackage

## Purpose

You can use notch to quickly configure logging for your Python application. I designed notch
to encapsulate and standardize logging configuration for Python applications that are deployed
as container workloads. The default settings work in many simple cases, and you can further
customize logging behavior with environment variables.

## Usage

Import notch and call `configure()` to configure logging in your application entrypoint.

```python
import notch

notch.configure()
```

Call `configure()` as early as possible in your application startup, because notch in turn
calls `logging.basicConfig()` to configure the logging system.

Using the default settings, notch will configure the root logger to send logs to
`sys.stdout`, set the log level to `INFO`, and set the log format to
`'%(levelname)s [%(name)s] %(message)s'`.

## Configuration

You can change the behavior of notch by setting environment variables.

* `LOG_LEVEL`: change the log level for the root logger. This can be any level the Python
  logging module recognizes: `DEBUG`, `INFO` (the default), `WARNING`, `ERROR`, or `CRITICAL`.
* `LOG_FORMAT`: change the format for log output. Use any placeholders defined in the
  [Python logging documentation][a].
* `OTHER_LOG_LEVELS`: change the log level for loggers other than the root logger. See the
  explanation below.

[a]: https://docs.python.org/3/library/logging.html#logrecord-attributes

## Setting log levels for other modules

If you use third-party packages, you may want to set log levels for these packages
independently. For example, you may want to see `DEBUG` logs for your own code, but only
`WARNING` messages for other modules. You can do this by setting the `OTHER_LOG_LEVELS`
environment variable.

The value of this variable should be a module name and a log level separated by a colon.
You can set log levels for multiple modules by separating entries with a space.

```
OTHER_LOG_LEVELS=first_module:WARNING second_module:ERROR
```

For a concrete example, if your application depends on `boto3` but you only want to see errors
from `boto3`-related modules in your logs, configure like this:

```
OTHER_LOG_LEVELS=boto3:ERROR botocore:ERROR
```

You can specify submodules as well if you need to be more specific:

```
OTHER_LOG_LEVELS=apscheduler.scheduler:WARNING
```
