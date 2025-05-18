import os
import json
import time
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import git  # GitPython must be installed: pip install GitPython

class BlockchainForkGUI:
    def __init__(self, master):
        self.master = master
        master.title("Blockchain Fork and Genesis Creator")

        # Row 0: Git Repository URL
        tk.Label(master, text="Git Repository URL:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_git_url = tk.Entry(master, width=50)
        self.entry_git_url.grid(row=0, column=1, padx=5, pady=5)
        self.entry_git_url.insert(0, "https://github.com/ethereum/go-ethereum.git")

        # Row 1: Clone Destination Directory with browse facility
        tk.Label(master, text="Clone Destination Directory:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_clone_dir = tk.Entry(master, width=50)
        self.entry_clone_dir.grid(row=1, column=1, padx=5, pady=5)
        self.entry_clone_dir.insert(0, os.getcwd())
        tk.Button(master, text="Browse", command=self.browse_clone_dir).grid(row=1, column=2, padx=5, pady=5)

        # Row 2: Blockchain Name
        tk.Label(master, text="Blockchain Name:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_name = tk.Entry(master, width=30)
        self.entry_name.grid(row=2, column=1, padx=5, pady=5)
        self.entry_name.insert(0, "MyEthereumFork")

        # Row 3: Consensus Mechanism
        tk.Label(master, text="Consensus Mechanism:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.consensus_var = tk.StringVar(master)
        self.consensus_var.set("Proof of Work (PoW)")
        consensus_options = ["Proof of Work (PoW)", "Proof of Stake (PoS)", "Hybrid", "Other"]
        tk.OptionMenu(master, self.consensus_var, *consensus_options).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Row 4: Difficulty
        tk.Label(master, text="Mining Difficulty:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.entry_difficulty = tk.Entry(master, width=30)
        self.entry_difficulty.grid(row=4, column=1, padx=5, pady=5)
        self.entry_difficulty.insert(0, "20000000000")

        # Row 5: Block Time (seconds)
        tk.Label(master, text="Block Time (seconds):").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.entry_blocktime = tk.Entry(master, width=30)
        self.entry_blocktime.grid(row=5, column=1, padx=5, pady=5)
        self.entry_blocktime.insert(0, "15")

        # Row 6: Block Reward
        tk.Label(master, text="Block Reward:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.entry_reward = tk.Entry(master, width=30)
        self.entry_reward.grid(row=6, column=1, padx=5, pady=5)
        self.entry_reward.insert(0, "2")

        # Row 7: Maximum Supply
        tk.Label(master, text="Max Supply:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.entry_max_supply = tk.Entry(master, width=30)
        self.entry_max_supply.grid(row=7, column=1, padx=5, pady=5)
        self.entry_max_supply.insert(0, "100000000")

        # Row 8: Genesis Timestamp (optional)
        tk.Label(master, text="Genesis Timestamp (optional):").grid(row=8, column=0, sticky="e", padx=5, pady=5)
        self.entry_timestamp = tk.Entry(master, width=30)
        self.entry_timestamp.grid(row=8, column=1, padx=5, pady=5)
        self.entry_timestamp.insert(0, str(int(time.time())))

        # Row 9: Additional JSON Config
        tk.Label(master, text="Additional Config (JSON format):").grid(row=9, column=0, sticky="ne", padx=5, pady=5)
        self.text_additional = tk.Text(master, height=6, width=30)
        self.text_additional.grid(row=9, column=1, padx=5, pady=5)
        self.text_additional.insert("1.0", '{"gasLimit": 8000000}')

        # Row 10: Logo File Selection
        tk.Label(master, text="Logo File (image path):").grid(row=10, column=0, sticky="e", padx=5, pady=5)
        self.entry_logo = tk.Entry(master, width=30)
        self.entry_logo.grid(row=10, column=1, padx=5, pady=5)
        tk.Button(master, text="Browse", command=self.browse_logo).grid(row=10, column=2, padx=5, pady=5)

        # Button to start the clone-and-fork procedure
        tk.Button(master, text="Clone and Fork Blockchain", command=self.clone_and_fork).grid(row=11, column=1, pady=10)

        # Status Message Area
        self.status_label = tk.Label(master, text="", fg="green", wraplength=500, justify="left")
        self.status_label.grid(row=12, column=0, columnspan=3, padx=5, pady=10)

    def browse_clone_dir(self):
        directory = filedialog.askdirectory(title="Select Clone Destination Directory")
        if directory:
            self.entry_clone_dir.delete(0, tk.END)
            self.entry_clone_dir.insert(0, directory)

    def browse_logo(self):
        filepath = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")]
        )
        if filepath:
            self.entry_logo.delete(0, tk.END)
            self.entry_logo.insert(0, filepath)

    def clone_and_fork(self):
        try:
            self.status_label.config(text="Starting cloning process...", fg="blue")
            self.master.update()

            # Gather repository parameters
            repo_url = self.entry_git_url.get().strip()
            base_clone_dir = self.entry_clone_dir.get().strip()

            # Derive repository name from URL
            repo_name = os.path.basename(repo_url)
            if repo_name.endswith(".git"):
                repo_name = repo_name[:-4]
            clone_path = os.path.join(base_clone_dir, repo_name)

            # Clone the repository
            self.status_label.config(text=f"Cloning repository into {clone_path}...", fg="blue")
            self.master.update()
            repo = git.Repo.clone_from(repo_url, clone_path)
            self.status_label.config(text="Repository cloned successfully.", fg="green")
            self.master.update()

            # Determine the branch: prefer 'master', fall back to 'main'
            branch_name = None
            if "master" in repo.heads:
                branch_name = "master"
            elif "main" in repo.heads:
                branch_name = "main"
            else:
                branch_name = repo.active_branch.name

            self.status_label.config(text=f"Using branch '{branch_name}' for commit search.", fg="green")
            self.master.update()

            # Define a cutoff date for PoW (for example, the Ethereum merge on September 15, 2022)
            cutoff = datetime.datetime(2022, 9, 15, tzinfo=datetime.timezone.utc)
            last_pow_commit = None

            # Iterate over commits from the branch's HEAD
            for commit in repo.iter_commits(branch_name):
                if commit.committed_datetime < cutoff:
                    last_pow_commit = commit
                    break

            if last_pow_commit is None:
                raise Exception("Could not find a commit before the cutoff date—ensure the repo history includes PoW commits.")

            # Checkout the found commit
            repo.git.checkout(last_pow_commit.hexsha)
            commit_info = f"Using commit {last_pow_commit.hexsha[:8]} dated {last_pow_commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
            current_status = f"Repository is now set to the last PoW commit:\n{commit_info}"
            self.status_label.config(text=current_status, fg="green")
            self.master.update()

            # ------------------------------------------------------------
            # Now, gather blockchain configuration parameters from the GUI
            blockchain_name = self.entry_name.get().strip()
            consensus = self.consensus_var.get()
            difficulty = int(self.entry_difficulty.get().strip())
            block_time = int(self.entry_blocktime.get().strip())
            reward = float(self.entry_reward.get().strip())
            max_supply = int(self.entry_max_supply.get().strip())
            timestamp_val = self.entry_timestamp.get().strip()
            timestamp = int(timestamp_val) if timestamp_val else int(time.time())
            additional_config_text = self.text_additional.get("1.0", tk.END).strip()
            additional_config = json.loads(additional_config_text) if additional_config_text else {}
            logo = self.entry_logo.get().strip()

            # Build a genesis configuration dictionary
            genesis_config = {
                "chainName": blockchain_name,
                "baseCommit": {
                    "hash": last_pow_commit.hexsha,
                    "message": last_pow_commit.message.strip(),
                    "date": last_pow_commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')
                },
                "consensus": consensus,
                "parameters": {
                    "difficulty": difficulty,
                    "blockTime": block_time,
                    "blockReward": reward,
                    "maxSupply": max_supply,
                    "genesisTimestamp": timestamp
                },
                "logo": logo,
                "additionalConfig": additional_config
            }

            # Save the configuration to a JSON file
            output_file = os.path.join(clone_path, f"{blockchain_name}_genesis.json")
            with open(output_file, "w") as f:
                json.dump(genesis_config, f, indent=4)

            success_msg = f"Fork successful!\n{commit_info}\n\nGenesis configuration file saved to:\n{output_file}"
            self.status_label.config(text=success_msg, fg="green")
            messagebox.showinfo("Success", success_msg)

        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.status_label.config(text=error_msg, fg="red")
            messagebox.showerror("Error", error_msg)

if __name__ == "__main__":
    root = tk.Tk()
    gui = BlockchainForkGUI(root)
    root.mainloop()