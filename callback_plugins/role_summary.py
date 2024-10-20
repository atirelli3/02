from ansible.plugins.callback import CallbackBase
import sys

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'role_summary'

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.role_results = {}
        self.current_role = None
        self.total_width = 80  # Lunghezza totale desiderata della riga

    def v2_playbook_on_task_start(self, task, is_conditional):
        role_name = task._role.get_name() if task._role else 'No Role'
        task_name = task.get_name()

        # Cambia il ruolo corrente e stampa l'intestazione del nuovo ruolo
        if role_name != self.current_role:
            self.current_role = role_name
            self._print_role_header(role_name)

        print(f"    - {task_name}: ", end="")

    def v2_runner_on_ok(self, result):
        print("\033[92mok\033[0m")  # Colore verde per ok

    def v2_runner_on_failed(self, result, ignore_errors=False):
        print("\033[91mfailed\033[0m")  # Colore rosso per failed

    def v2_runner_on_skipped(self, result):
        print("\033[93mskipped\033[0m")  # Colore giallo per skipped

    def _print_role_header(self, role_name):
        # Calcola quanti asterischi sono necessari per arrivare a 80 caratteri
        header = f"ROLE [{role_name.upper()}] "
        num_stars = self.total_width - len(header)
        print(f"{header}{'*' * num_stars}")

    def _update_task_status(self, role, task_name, status):
        for task in self.role_results[role]:
            if task['task'] == task_name:
                task['status'] = status
                break

    def _get_color_for_status(self, status):
        if status == 'ok':
            return "\033[92m"  # Verde per ok
        elif status == 'failed':
            return "\033[91m"  # Rosso per failed
        elif status == 'skipped':
            return "\033[93m"  # Giallo per skipped
        return ""
