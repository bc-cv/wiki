Andromeda Linux Cluster
=======================
The `Andromeda Linux Cluster <https://www.bc.edu/bc-web/offices/its/services/research-services/linux-cluster.html>`_ runs the SLURM scheduler to execute jobs.

Connecting to the cluster
-------------------------
- Secure SHell (SSH) into the root node of Andromeda (``l001``)

   .. code-block:: none
   
      > ssh {user}@andromeda.bc.edu -p 22022

- To SSH into ``{node}`` in the ``l001`` shell

   .. code-block:: none
   
      > ssh {node}

- To forward X11 from ``l001`` (not recommended; either host a webpage whose port can be exposed or setup NoMachine)

   .. code-block:: none
   
      > ssh -X {user}@andromeda.bc.edu -p 22022

- Expose a port on ``l001`` (e.g., to access a Jupyter/Neuroglancer server)

   .. code-block:: none
   
      > ssh -L {local_port}:localhost:{remote_port} -N -T {user}@andromeda.bc.edu -p 22022

- Expose a port on ``{node}`` (e.g., to access a service run by a job)

   .. code-block:: none
   
      > ssh -t -t {user}@andromeda.bc.edu -p 22022 -L {local_port}:localhost:{unused_port} ssh -T -N {node} -L {unused_port}:localhost:{remote_port}

- To mount the cluster's filesystem locally (e.g., enabling use of local development environment)

   - Linux:

      .. code-block:: none
      
         > sudo umount -l {local_mount_point}; sshfs {user}@andromeda.bc.edu:{remote_path} {local_mount_point} -p 22022

   - MacOS: Install `FUSE for macOS <https://osxfuse.github.io/>`_ and their SSHFS plugin
   - Windows: Install `sshfs-win <https://github.com/winfsp/sshfs-win>`_

- It is recommended to setup `passwordless SSH login <https://stackoverflow.com/a/21467504/10702372>`_ for both convenience and security

Filesystem
----------
- ``/mmfs1/data/bccv``: BC-CV's main directory, used to share dataset files etc.
- ``/mmfs1/data/{user}``: home directory on NFS; backed up daily; other users have no access
- ``/scratch/{user}``: directory on NFS to store (large) temporary files; not backed up; other users have access (can be used to share files)
- ``/local``: directory **specific to each node** (``/local`` is different on ``l001`` and ``g001``); usage is discouraged

Modules
-------
Andromeda uses the `Modules package <https://modules.readthedocs.io/en/latest/>`_ to manage packages that influence the shell environment.

- List available modules

   .. code-block:: none
   
      > module avail

- Load a module to make commands available

   .. code-block:: none
   
      > module load {module}
- Unload all modules

   .. code-block:: none
   
      > module purge

To avoid having to load modules every time you SSH, you can append the ``module load`` commands at the end of your ``~/.tcshrc`` file.

Conda
-----
It is recommended to use Conda to manage Python packages to ensure reproducibility and minimize conflicts between project dependencies. For a primer on Conda see the following `cheatsheet <https://conda.io/projects/conda/en/latest/user-guide/cheatsheet.html>`_ To use Conda, load the ``anaconda`` module.

Useful commands:

- List all environments

   .. code-block:: none
   
      > conda info --envs   
- Create a new environment

   .. code-block:: none
  
      > conda create --name {env_name} python={version}
- Activate an environment

   .. code-block:: none

      > conda activate {env_name}
- Install packages in current environment

   .. code-block:: none

      > conda install {package1} {package2} ...
- Uninstall packages in current environment

   .. code-block:: none

      > conda uninstall {package1} {package2} ...

Using `Mamba <https://mamba.readthedocs.io/en/latest/installation.html>`_ (a drop-in replacement for Conda) can significantly speed up package installation.

SLURM
-----
Although long running tasks can technically be run on ``l001`` (by using ``screen`` or ``tmux``), computationally intensive jobs should be run through SLURM scheduler. To use SLURM, load the ``slurm`` module.

- To view statuses of nodes on all partitions (e.g., to find idle partitions)

   .. code-block:: none

      > sinfo
- To view detailed stats of nodes on all partitions (e.g., to find available RAM/number of cores per node)

   .. code-block:: none

      > sinfo --Node --long
- To view all queued jobs

   .. code-block:: none
  
      > squeue
- To view your queued jobs

   .. code-block:: none

      > squeue -u {user}
- To submit a job

   .. code-block:: none

      > sbatch {job_script}

   An example SLURM job script (`more details <https://slurm.schedmd.com/sbatch.html>`_):

      .. code-block:: bash

         #!/bin/tcsh -e
         #SBATCH --job-name=example-job # job name
         #SBATCH --nodes=1 # how many nodes to use for this job
         #SBATCH --ntasks=1
         #SBATCH --cpus-per-task 48 # how many CPU-cores to use for this job (see )
         #SBATCH --mem=190GB # how much RAM to allocate
         #SBATCH --time=120:00:00 # job execution time limit hrs:min:sec
         #SBATCH --mail-type=BEGIN,END,FAIL. # mail events (NONE, BEGIN, END, FAIL, ALL)
         #SBATCH --mail-user={user}@bc.edu # where to send mail
         #SBATCH --partition=partial_nodes,gpuv100,gpua100 # see sinfo for available partitions

         #SBATCH --output=main_%j.out 

         module purge # clear all modules
         module load slurm # to allow sub-scripts to use SLURM commands
         module load cuda11.2 # for gpuv100/gpua100 partitions only

         module load anaconda
         conda activate clean_dendrite

         hostname # print the node which the job is running on

         ...

- To run a job script `interactively <https://stackoverflow.com/questions/43767866/slurm-srun-vs-sbatch-and-their-parameters>`_ (e.g., for ``pdb`` debugging)

   .. code-block:: none

      > srun {flags} {job_script}
   
   Note that ``srun`` does not read the ``#SBATCH`` directives in the job script; flags must be specified manually.


