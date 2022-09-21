EM-Connectomics
================
TODO: add a summary table


SNEMI3D: Segmentation
--------------------------
- Description
    - resolution: 6x6x30 nm

    - train: 6x6x3 um (AC4 in `Kasthuri dataset <https://software.rc.fas.harvard.edu/lichtman/vast/>`_) 

        - ``image/train-input.tif``, ``seg/train-labels.tif``

    - test: 6x6x3 um (first 100 slices in AC3 in `Kasthuri dataset <https://software.rc.fas.harvard.edu/lichtman/vast/>`_) 

        - ``image/test-input.tif``
- Download
    - `snemi website <http://brainiac2.mit.edu/SNEMI3D/user/register>`_ (register first)

    - `Rhoana copy <http://hp03.mindhackers.org/rhoana_product/dataset/snemi.zip>`_

    - RC server copy: ``/n/coxfs01/vcg_connectomics/snemi/``

    - valid: 6x6x4 um (last 156 slices in AC3 in `Kasthuri dataset <https://software.rc.fas.harvard.edu/lichtman/vast/>`_) 


CREMI: Segmentation+Synapse
-------------------------------
- Description
    - resolution: 4x4x40 nm

    - train: 5x5x5 um

           - ``orig/sample_{A,B,C}_20160501.hdf``
    - test: 5x5x5 um

           - ``orig/sample_{A,B,C}+_20160601.hdf``
    - correction:

           - shift re-alignment all volumes

           - {A,B,C}: crop the intersecting regions

           - A+: fix the crack
- Download
   - `cremi website <https://cremi.org/data/>`_

   - `Rhoana copy (corrected) <http://hp03.mindhackers.org/rhoana_product/dataset/cremi.zip>`_

   - RC server (corrected): ``/n/coxfs01/vcg_connectomics/cremi/``

LUCCHI: Mitochondria
---------------------
- Description
    - resolution: 5x5x5 nm

    - train: 5x4x1 um

           - ``train_im.tif``, ``train_label.tif``
    - test: 5x5x5 um

           - ``test_im.tif``, ``test_label.tif``
- Download
   - `lucchi website <https://cvlab.epfl.ch/data/data-em/>`_

   - `Rhoana copy <http://hp03.mindhackers.org/rhoana_product/dataset/lucchi.zip>`_

   - RC server (corrected): ``/n/coxfs01/vcg_connectomics/mitochondria/Lucchi/``
