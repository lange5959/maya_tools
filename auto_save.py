# coding=utf8

import os
import shutil
import time
import traceback
import pymel.core as pm
import maya.OpenMaya as om


def backup_before_save(*args):
    if not pm.sceneName():
        return
    current_path = om.MFileIO().currentFile()
    name = os.path.basename(current_path)
    parent_path = os.path.dirname(current_path)
    folder_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    new_path = os.path.join(parent_path, 'backupSave', folder_name)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_ma_path = os.path.join(new_path, name)
    if current_path and os.path.exists(current_path):
        try:
            shutil.copy(current_path, new_ma_path)
        except:
            traceback.print_exc()
            print('\n'*10)


def auto_save(*args):
    """
    """
    if not pm.sceneName():
        return
    if pm.dgmodified():
        pm.saveFile()
    pm.inViewMessage(
        amg=u'自动保存 <hl>完成</hl>.',
        pos='midCenter',
        fade=True)


time_callback_id = om.MTimerMessage.addTimerCallback(
    30*60, auto_save)


id_before_save = om.MSceneMessage.addCallback(
    om.MSceneMessage.kBeforeSave, backup_before_save)

# 移除当前事件
# om.MTimerMessage.removeCallback(id_before_save)
# om.MMessage.removeCallback(time_callback_id)
