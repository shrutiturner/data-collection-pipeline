class Logger:

    @staticmethod
    def log_error(exception) -> None:
        with open('error_log.txt', 'a') as file:
            file.write(exception)
