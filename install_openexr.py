import os
import platform
import subprocess
import shutil
import errno

def run_command(cmd_arg_list, workdir_path):
    """
    Run a subprocess command.

    @param cmd_arg_list: A list of the command and its arguments.
    @param workdir: Absolute path to the working directory the command should be run in.
    @raises: subprocess.CallProcessError if an error occurred.
    """
    use_shell = ("Windows" in platform.system())

    process = subprocess.Popen(cmd_arg_list, stdout=subprocess.PIPE, universal_newlines=True, shell=use_shell,
                               cwd=workdir_path)
    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line.rstrip())
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, ' '.join(cmd_arg_list))

def create_dir(dir_path):
    """
    Create a directory if it doesn't exist. This calls os.makedirs() and creates all ancestor dirs.

    @param dir_path: Absolute path of the directory that should be created.
    """
    try:
        os.makedirs(dir_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir_path):
            pass
        else:
            raise

def copy_dir(src_dir, dst_dir):
    """
    Copy directory like shutil.copytree.  It replaces the contents of dst_dir completely with the contents of src_dir.


    @param src_dir: The absolute path to the source directory to copy.
    @param dst_dir: The absolute path to the destination directory to copy.
    """
    if os.path.isdir(dst_dir):
        print("Removing previous copy of {dst_dir}".format(dst_dir=dst_dir))
        shutil.rmtree(dst_dir)
    print("Copying {src_dir} to {dst_dir}\n".format(src_dir=src_dir, dst_dir=dst_dir))
    shutil.copytree(src_dir, dst_dir)


# Entry point
if __name__ == '__main__':
    for key,value in os.environ.items():
        if key.startswith('REZ_BUILD_'):
            print("{} = {}".format(key, value))

    for key,value in os.environ.items():
        if key.find('__PARSE_ARG_') >= 0:
            print("{} = {}".format(key, value))

    for key,value in os.environ.items():
        if value.find('Ninja') >= 0:
            print("{} = {}".format(key, value))

    # Configure IlmBase CMake.
    IlmBase_build_path = os.path.join(os.environ.get('REZ_BUILD_PATH'), 'IlmBase')
    create_dir(IlmBase_build_path)
    if int(os.environ['REZ_BUILD_INSTALL']) != 0:
        inst_dir = os.environ.get('REZ_BUILD_INSTALL_PATH')
    else:
        inst_dir = IlmBase_build_path
    cmake_cmd_list = [
        'cmake',
        '-g "Ninja"',
        '-DCMAKE_BUILD_TYPE={}'.format(os.environ.get('__PARSE_ARG_BUILD_CONFIG')),
        '-DCMAKE_VERBOSE_MAKEFILE={}'.format(os.environ.get('__PARSE_ARG_BUILD_VERBOSE')),
        '-DCMAKE_INSTALL_PREFIX={}'.format(inst_dir),
        os.path.join(os.environ.get('REZ_BUILD_SOURCE_PATH'), 'IlmBase')
    ]
    run_command(cmake_cmd_list, IlmBase_build_path)

    # Do IlmBase build.
    cmake_cmd_list = ['cmake', '--build', '.']
    if int(os.environ.get('__PARSE_ARG_BUILD_JOBS_NUM')) > 0:
        cmake_cmd_list.append('--')
        cmake_cmd_list.append('-j{}'.format(os.environ.get('__PARSE_ARG_BUILD_JOBS_NUM')))
    run_command(cmake_cmd_list, IlmBase_build_path)

    # Always do Ilmbase REZ package installation.... but do it to the ${REZ_BUILD_PATH}/IlmBase so that
    # the OpenEXR can refer to it with ILMBASE_PACKAGE_PREFIX.
    #if int(os.environ['REZ_BUILD_INSTALL']) != 0:
    cmake_cmd_list = ['cmake', '--install', '.', '--prefix', inst_dir]
    run_command(cmake_cmd_list, IlmBase_build_path)

    # Configure OpenEXR CMake.
    OpenEXR_build_path = os.path.join(os.environ.get('REZ_BUILD_PATH'), 'OpenEXR')
    create_dir(OpenEXR_build_path)
    cmake_cmd_list = [
        'cmake',
        '-g "Ninja"',
        '-DCMAKE_BUILD_TYPE={}'.format(os.environ.get('__PARSE_ARG_BUILD_CONFIG')),
        '-DCMAKE_VERBOSE_MAKEFILE={}'.format(os.environ.get('__PARSE_ARG_BUILD_VERBOSE')),
        '-DILMBASE_PACKAGE_PREFIX={}'.format(inst_dir),
        '-DCMAKE_INSTALL_PREFIX={}'.format(inst_dir),
        os.path.join(os.environ.get('REZ_BUILD_SOURCE_PATH'), 'OpenEXR')
    ]
    run_command(cmake_cmd_list, OpenEXR_build_path)

    # Do OpenEXR build.
    cmake_cmd_list = ['cmake', '--build', '.']
    if int(os.environ.get('__PARSE_ARG_BUILD_JOBS_NUM')) > 0:
        cmake_cmd_list.append('--')
        cmake_cmd_list.append('-j{}'.format(os.environ.get('__PARSE_ARG_BUILD_JOBS_NUM')))
    run_command(cmake_cmd_list, OpenEXR_build_path)

    # Do OpenEXR REZ package installation.
    if int(os.environ['REZ_BUILD_INSTALL']) != 0:
        cmake_cmd_list = ['cmake', '--install', '.', '--prefix', inst_dir]
        run_command(cmake_cmd_list, OpenEXR_build_path)
