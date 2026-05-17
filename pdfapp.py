import threading
from tkinter import Tk, Button, Label, filedialog, simpledialog, messagebox, StringVar, DISABLED, NORMAL
import os
import pikepdf


def protect_pdf():
    try:
        input_path = filedialog.askopenfilename(
            title="Select PDF to protect",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not input_path:
            return

        password = simpledialog.askstring("Password", "Enter password to set:", show="*")
        if not password:
            messagebox.showinfo("Cancelled", "No password entered.")
            return

        # Default output filename
        base, ext = os.path.splitext(os.path.basename(input_path))
        default_name = f"{base}_protected.pdf"

        output_path = filedialog.asksaveasfilename(
            title="Save protected PDF as",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF files", "*.pdf")],
        )
        if not output_path:
            return

        # Open and encrypt the PDF
        try:
            with pikepdf.open(input_path) as pdf:
                # Check if PDF is already encrypted
                if pdf.is_encrypted:
                    messagebox.showwarning(
                        "Warning",
                        "This PDF is already encrypted. Please decrypt it first or use a different PDF."
                    )
                    return
                
                pdf.save(
                    output_path,
                    encryption=pikepdf.Encryption(
                        user=password,
                        owner=password,
                        allow=pikepdf.Permissions(
                            extract=False,
                            accessibility=True,
                            modify_annotation=False,
                            modify_assembly=False,
                            modify_form=False,
                            modify_other=False,
                            print_lowres=True,
                            print_highres=False,
                        ),
                        R=4,
                    ),
                )
            messagebox.showinfo("Success", f"Protected PDF saved:\n{output_path}")
        except pikepdf.PasswordError:
            messagebox.showerror(
                "Error",
                "This PDF is password-protected. Please decrypt it first before adding a new password."
            )
            return
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        messagebox.showerror("Error", f"Failed to protect PDF:\n{error_msg}")


class PinCracker:
    def __init__(self, status_var: StringVar, crack_btn: Button):
        self.status_var = status_var
        self.crack_btn = crack_btn
        self._stop = False

    def crack_pdf_pin(self):
        input_path = filedialog.askopenfilename(
            title="Select password-protected PDF",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not input_path:
            return

        base, _ = os.path.splitext(os.path.basename(input_path))
        default_name = f"{base}_decrypted.pdf"

        output_path = filedialog.asksaveasfilename(
            title="Save decrypted PDF as",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF files", "*.pdf")],
        )
        if not output_path:
            return

        self.crack_btn.config(state=DISABLED)
        self.status_var.set("Starting brute force (0000–9999)...")

        def worker():
            try:
                found_pin = None
                for i in range(10000):
                    pin = f"{i:04d}"
                    if i % 50 == 0:
                        self.status_var.set(f"Trying PIN: {pin}")

                    try:
                        with pikepdf.open(input_path, password=pin) as pdf:
                            pdf.save(output_path)
                            found_pin = pin
                            break
                    except pikepdf.PasswordError:
                        continue
                    except Exception as e:
                        continue

                if found_pin is not None:
                    self.status_var.set(f"PIN found: {found_pin}")
                    messagebox.showinfo(
                        "Success",
                        f"PIN found: {found_pin}\nDecrypted PDF saved:\n{output_path}",
                    )
                else:
                    self.status_var.set("PIN not found within 0000–9999.")
                    messagebox.showwarning(
                        "Not Found",
                        "Could not crack PIN in range 0000–9999.",
                    )
            finally:
                self.crack_btn.config(state=NORMAL)

        t = threading.Thread(target=worker, daemon=True)
        t.start()


def main():
    root = Tk()
    root.title("PDF Protector & 4-digit PIN Cracker")
    root.geometry("460x220")

    title = Label(root, text="PDF Protector & PIN Cracker", font=("Segoe UI", 14, "bold"))
    title.pack(pady=10)

    status_var = StringVar(value="Ready.")
    status_label = Label(root, textvariable=status_var, wraplength=420, justify="left")
    status_label.pack(pady=5)

    protect_btn = Button(root, text="Protect PDF", width=24, command=protect_pdf)
    protect_btn.pack(pady=6)

    crack_btn = Button(root, text="Crack 4-digit PIN", width=24)
    cracker = PinCracker(status_var, crack_btn)
    crack_btn.config(command=cracker.crack_pdf_pin)
    crack_btn.pack(pady=6)

    footer = Label(root, text="Note: Cracking tries PINs 0000–9999", fg="#666")
    footer.pack(pady=6)

    root.mainloop()


if __name__ == "__main__":
    main()