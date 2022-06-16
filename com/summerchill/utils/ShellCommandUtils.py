import os;
def shell_cmd_execute(shell_cmd):
    """
    执行shell命令
    """
    os.system(shell_cmd)

# ***该类的入口main方法
if __name__ == "__main__":
    shell_cmd = 'java -jar /Users/kongxiaohan/project_code/idea/longfor/cryption/target/cryption-1.0-SNAPSHOT-jar-with-dependencies.jar 475036F12F6980BE3FB7FE73B4A05E1A66D65A9A5E40AEB4'
    shell_cmd_execute(shell_cmd)

