Andromeda Linux Cluster
=======================
The `Andromeda Linux Cluster <https://www.bc.edu/bc-web/offices/its/services/research-services/linux-cluster.html>`_ runs the SLURM scheduler to execute jobs.

.. note::
   If necessary, contact `Professor Wei <mailto:donglai.wei@bc.edu>`_ to request a BC ID. Additional information can be found on the `Boston College website <https://www.bc.edu/content/bc-web/offices/its/support/account-network-access/basics.html#tab-bc_password>`_

Connecting to the cluster
-------------------------
.. note:: If you are off campus, it's necessary to first connect to `Eagle VPN <https://bcservices.bc.edu/service/cisco-anyconnect-vpn>`_, which is available on Windows, Mac, and Linux.

Users can log into the cluster via Secure Shell. Below are some helpful commands:

- Connect to login node of Andromeda from local machine: ``ssh {user}@andromeda.bc.edu``
- Run an interactive bash shell from login node (CPU only): ``interactive``
- Run an interactive bash shell from login node (with GPU): ``srun -t 12:00:00 -N 1 -n 1 --mem=32gb --partition=gpua100 --gpus-per-node=1 --pty bash``
    
.. note:: Resources on the login node are limited and split among all users. Users spending a protracted session on the cluster are asked to run ``interactive`` as a courtesy to other users.

.. tip:: It is recommended to setup `passwordless SSH login <https://stackoverflow.com/a/21467504/10702372>`_ for both convenience and security


- To forward X11 from ``l001`` (not recommended; either host a webpage whose port can be exposed or setup NoMachine)

   .. code-block:: none
   
      > ssh -X {user}@andromeda.bc.edu

- Expose a port on ``l001`` (e.g., to access a Jupyter/Neuroglancer server)

   .. code-block:: none
   
      > ssh -L {local_port}:localhost:{remote_port} -N -T {user}@andromeda.bc.edu

- Expose a port on ``{node}`` (e.g., to access a service run by a job)

   .. code-block:: none
   
      > ssh -t -t {user}@andromeda.bc.edu -L {local_port}:localhost:{unused_port} ssh -T -N {node} -L {unused_port}:localhost:{remote_port}

- To mount the cluster's filesystem locally (e.g., enabling use of local development environment)

   - Linux:

      .. code-block:: none
      
         > sudo umount -l {local_mount_point}; sshfs {user}@andromeda.bc.edu:{remote_path} {local_mount_point}

   - MacOS: Install `FUSE for macOS <https://osxfuse.github.io/>`_ and their SSHFS plugin
   - Windows: Install `sshfs-win <https://github.com/winfsp/sshfs-win>`_


Filesystem
----------
- The BC-CV's main directory is located at ``/mmfs1/data/projects/weilab``. It's commonly used to share large files like datasets.
- The user home directory is located at  ``/mmfs1/data/{user}``. Daily backups are automatically made.
    
    - These backups are found at ``/mmfs1/data/{user}/.snapshots``.

- Each user has a directory ``/scratch/{user}`` that can store large temporary files. Unlike the home directory, it isn't backed up.

.. note:: Users should contact `Wei Qiu <mailto:qiuwa@bc.edu>`_ and ask to be added to Professor Wei's group in order to get access to ``/mmfs1/data/projects/weilab``.

Modules
-------
Andromeda uses the `Modules package <https://modules.readthedocs.io/en/latest/>`_ to manage packages that influence the shell environment.

- List available module: ``module avail``
- List loaded modules: ``module list``
- Load a module: ``module load {module}``
- Unload all modules: ``module purge``

.. tip:: To avoid having to load modules every time you SSH, you can append the ``module load`` commands at the end of your ``~/.tcshrc`` file.

Conda
-----
It is recommended to use Conda (a Python package manager) to minimize conflicts between projects' dependencies. For a primer on Conda see the following `cheatsheet <https://conda.io/projects/conda/en/latest/user-guide/cheatsheet.html>`_. To use Conda, load the ``anaconda`` module.

.. tip:: Using `Mamba <https://mamba.readthedocs.io/en/latest/installation.html>`_ (a drop-in replacement for Conda) can significantly speed up package installation.

SLURM
-----
Although long running tasks can technically be run on ``l001`` (by using ``screen`` or ``tmux``), computationally intensive jobs should be run through SLURM scheduler. To use SLURM, load the ``slurm`` module.

- To view statuses of all nodes: ``sinfo``
- To view detailed info of all nodes: ``sinfo --Node --long``
- To view all queued jobs: ``squeue``
- To view your queued jobs: ``squeue -u {user}``
- To submit a job: ``sbatch {job_script}``

A basic SLURM job script is provided below; more details can be found `here <https://slurm.schedmd.com/sbatch.html>`_.

.. code-block:: bash

    #!/bin/tcsh -e
    #SBATCH --job-name=example-job # job name
    #SBATCH --nodes=1 # how many nodes to use for this job
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task 48 # how many CPU-cores to use for this job
    #SBATCH --mem=128GB # how much RAM to allocate
    #SBATCH --time=120:00:00 # job execution time limit formatted hrs:min:sec
    #SBATCH --mail-type=BEGIN,END,FAIL. # mail events (NONE, BEGIN, END, FAIL, ALL)
    #SBATCH --mail-user={user}@bc.edu # where to send mail
    #SBATCH --partition=partial_nodes,gpuv100,gpua100 # see sinfo for available partitions

    #SBATCH --output=main_%j.out
    
    hostname # print the node which the job is running on

    module purge # clear all modules
    module load slurm # to allow sub-scripts to use SLURM commands
    module load anaconda

    conda activate {my_env}
    {more commands...}

Advanced
--------

Port Forwarding
###############

Port forwarding is useful for accessing services from a job (e.g. Jupyter notebooks, Tensorboard). Suppose that a user is running a service on node ``{node}`` that is exposed to port ``{port_2}``. To recieve the node's services on your local machine:

.. code-block:: bash
   
    ssh {user}@andromeda.bc.edu -L {local_port}:localhost:{port_1} ssh -T -N {node} -L {port_1}:localhost:{port_2}


FAQ
---
- **Q:** My SLURM jobs running Python raises ``ImportError:`` despite having ``module load anaconda; conda activate {my_env}``

   **A:** Try adding ``which python`` to the beginning of the script to see which Python binary is being used. If it is not the binary of your conda environment, hardcode the path to the Python binary.

- **Q:** My PyTorch model returns incorrect numerical results when running on A100 nodes but work fine on V100 nodes

   **A:** Add the following lines to your Python script (`source <https://discuss.pytorch.org/t/numerical-error-on-a100-gpus/148032>`_):

   .. code-block:: python

      import torch
      torch.backends.cuda.matmul.allow_tf32 = False
      torch.backends.cudnn.allow_tf32 = False
