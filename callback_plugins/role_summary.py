from ansible.plugins.callback import CallbackBase
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

class Loader:
    def __init__(self, desc="Loading...", end="", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print (left blank to prevent extra lines).
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def stop(self):
        self.done = True
        # Pulisci la linea del loader ma non stampare nulla
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'role_summary'

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.role_results = {}
        self.current_role = None
        self.total_width = 80  # Lunghezza totale desiderata della riga
        self.loader = None  # Per gestire il loader

    def v2_playbook_on_task_start(self, task, is_conditional):
        role_name = task._role.get_name() if task._role else 'No Role'
        task_name = task.get_name()

        # Cambia il ruolo corrente e stampa l'intestazione del nuovo ruolo
        if role_name != self.current_role:
            self.current_role = role_name
            self._print_role_header(role_name)

        # Avvia l'animazione del loader per il task
        self.loader = Loader(f"    - {task_name}", timeout=0.1).start()

    def v2_runner_on_ok(self, result):
        if self.loader:
            self.loader.stop()
        print(f"\r    - {result._task.get_name()}: \033[92mok\033[0m")  # Colore verde per ok

    def v2_runner_on_failed(self, result, ignore_errors=False):
        if self.loader:
            self.loader.stop()

        # Stampa il risultato con il messaggio di errore
        error_message = result._result.get('msg', 'Task failed')  # Ottieni il messaggio di errore
        print(f"\r    - {result._task.get_name()}: \033[91mFAILED! => {error_message}\033[0m")  # Colore rosso per failed

    def v2_runner_on_skipped(self, result):
        if self.loader:
            self.loader.stop()
        print(f"\r    - {result._task.get_name()}: \033[93mskipped\033[0m")  # Colore giallo per skipped

    def _print_role_header(self, role_name):
        # Calcola quanti asterischi sono necessari per arrivare a 80 caratteri
        header = f"ROLE [{role_name.upper()}] "
        num_stars = self.total_width - len(header)
        print(f"{header}{'*' * num_stars}")
