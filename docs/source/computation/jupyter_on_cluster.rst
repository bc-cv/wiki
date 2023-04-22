Running Jupyter lab on Andromeda
=================================
#. Login to Andromeda and forward a port from your local computer to the login node. This port will be used for Jupyter Lab

   .. code-block:: none

        ssh -L <port number>:localhost:<port number> <username>@andromeda.bc.edu
    
#. Launch a batch job from the cluster with the necessary parameters in the desired node. A sample batch file with the required commands are given below

   .. code-block:: none

      #!/bin/tcsh -e
      #SBATCH --job-name=jupyter_server
      #SBATCH --nodes=1
      #SBATCH --cpus-per-task=6
      #SBATCH --mem=8GB
      #SBATCH --time=00:10:00
      #SBATCH --partition=fullnodes48
      #SBATCH -o jupyter.out # Make sure this parameter is set

      # This will set the jupyter kernel to the right python version
      # You can alternatively choose to load desired modules
      conda activate <env>
      
      # Do not delete this line
      # It essentially reverse tunnels a port from the allocated node to the login node
      ssh -N -n -f -R <port number>:localhost:<port number> $USER@l001 
      
      jupyter notebook --no-browser --port=<port number>

#. Once the job is allocated and running, find the server address in jupyter.out. Paste that in a browser on your local computer and the Jupyter Interface should start up


Ensure that you do not close the terminal with the forwarded port. In case you do close it, forward the port again as shown in step 1 and you should be set. 
