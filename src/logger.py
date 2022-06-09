class Logger:

    @staticmethod
    def log_error(exception) -> None:
        """Writes errors raised to a text file for logging.

        Args:
            exception (error): The error that has been raised.
        """
        with open('error_log.txt', 'a') as file:
            file.write(exception)

        return None