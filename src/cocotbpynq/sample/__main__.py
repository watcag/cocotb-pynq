
def main():
    import subprocess
    has_sim_build = "sim_build" in subprocess.run(["ls", "-d", "./sim_build"], capture_output=True, text=True).stdout

    import cocotbpynq.sample.cocotb_runner

    if not has_sim_build: # Don't delete sim_build dir if it was pre-existing
        subprocess.run(["rm", "-rf", "./sim_build"])

if __name__ == "__main__":
    main()