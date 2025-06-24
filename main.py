import subprocess
import sys

#图形界面输出(模块化)
def run_gui():
    print("正在启动图形界面 (Streamlit)...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app_gui.py"])

if __name__ == "__main__":
    # 直接启动图形界面
    run_gui()

    # 使用命令行
    # main_cli()
