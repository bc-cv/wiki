Andromeda Linux Cluster
=======================
The `Andromeda Linux Cluster https://www.bc.edu/bc-web/offices/its/services/research-services/linux-cluster.html`_ runs the SLURM scheduler to execute jobs.

Connecting to the cluster
-------------------------
- Secure SHell (SSH) into the root node of Andromeda (``l001``)

   .. code-block:: none
   
      ssh {user}@andromeda.bc.edu -p 22022

- To SSH into ``{node}`` **in the ``l001``` shell**

   .. code-block:: none
   
      ssh {node}

- To forward X11 from ``l001`` (not recommended; either host a webpage whose port can be exposed or setup NoMachine)

   .. code-block:: none
   
      ssh -X {user}@andromeda.bc.edu -p 22022

- Expose a port on ``l001`` (e.g., to access a Jupyter/Neuroglancer server)

   .. code-block:: none
   
      ssh -L {local_port}:localhost:{remote_port} -N -T {user}@andromeda.bc.edu -p 22022

- Expose a port on ``{node}`` (e.g., to access a service run by a job)

   .. code-block:: none
   
      ssh -t -t {user}@andromeda.bc.edu -p 22022 -L {local_port}:localhost:{unused_port} ssh -T -N g006 -L {unused_port}:localhost:{remote_port}

- To mount the cluster's filesystem locally (e.g., enabling use of local development environment)

   - Linux:

      .. code-block:: none
      
         sudo umount -l {local_mount_point}; sshfs {user}@andromeda.bc.edu:{remote_path} {local_mount_point} -p 22022

   - MacOS: Install `FUSE for macOS https://osxfuse.github.io/`_ and their SSHFS plugin
   - Windows: Install `sshfs-win https://github.com/winfsp/sshfs-win`_

- It is recommended to setup `passwordless SSH login https://stackoverflow.com/a/21467504/10702372`_ for both convenience and security

Filesystem
----------
- ``/mmfs1/data/bccv``: BC-CV's main directory, used to share dataset files etc.
- ``/mmfs1/data/{user}``: home directory on NFS; backed up daily; other users have no access
- ``/scratch/{user}``: directory on NFS to store (large) temporary files; not backed up; other users have access (can be used to share files)
- ``/local``: directory **specific to each node** (``/local`` is different on ``l001`` and ``g001``); usage is discouraged

Modules
-------
Andromeda uses the `Modules package https://modules.readthedocs.io/en/latest/`_ to manage packages that influence the shell environment.

- ``module avail``: list available modules
- ``module load {module}``: load a module, making its binaries available
- ``module purge``: unload all modules

To avoid having to load modules every time you SSH, you can append the ``module load`` commands to the end of your ``~/.bashrc`` file.

Conda
-----
It is recommended to use Conda to manage Python packages to ensure reproducibility and minimize conflicts between project dependencies. For a primer on Conda see the following `cheatsheet https://conda.io/projects/conda/en/latest/user-guide/cheatsheet.html`_
Useful commands:
- ``conda info --envs``: list available environments
- ``conda create -n {env_name} python={version}``: create a new environment
- ``conda activate {env_name}``: activate an environment
- ``conda install {package1} {package2} ...``: install packages in the current environment
- ``conda uninstall {package1} {package2} ...``: uninstall packages in the current environment

Using `Mamba https://mamba.readthedocs.io/en/latest/installation.html`_ (a drop-in replacement for ``conda``) can significantly speed up package installation.

SLURM
-----
Although long running tasks can technically be run on ``l001`` (by using ``screen`` or ``tmux``), computationally intensive jobs should be run through SLURM scheduler.