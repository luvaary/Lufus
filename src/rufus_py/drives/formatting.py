import subprocess
import sys
from pathlib import Path
from rufus_py.drives import states
from rufus_py.drives import find_usb as fu
#######


mount_dict = fu.find_usb()  # GETS THE FIRST KEY FOR NOW
if mount_dict:
    mount = next(iter(mount_dict))  # IMPORT THE INITIAL MOUNT POINT
    drive = fu.find_DN() # IMPORTS DRIVE NODE
else:
    mount=None
    drive=None

def pkexecNotFound():
    print("Error: The command pkexec or labeling software was not found on your system.")
def FormatFail():
    print("Error: Formatting failed. Was the password correct? Is the drive unmounted?")
def unexpected():
    print(f"An unexpected error occurred")

    # 0 -> NTFS 
    # 1 -> FAT32 
    # 2 -> exFAT
    # 3 -> ext4

# UNMOUNT FUNCTION
def unmount():
    try:
        subprocess.run(["umount", drive], check=True)
    # except FileNotFoundError:
    #     pkexecNotFound()
    except subprocess.CalledProcessError:
        FormatFail()
    except Exception as e:
        print(f"(UMNTFUNC) DEBUG: Unexpected error type: {type(e).__name__}")
        print(f"DEBUG: Error message: {e}")
        unexpected() 
# MOUNT FUNCTION
def remount():
    try:
        subprocess.run(["mount", drive, mount], check=True)
    # except FileNotFoundError:
    #     pkexecNotFound()
    except subprocess.CalledProcessError:
        FormatFail()
    except Exception as e:
        print(f"(MNTFUNC) DEBUG: Unexpected error type: {type(e).__name__}")
        print(f"DEBUG: Error message: {e}")
        unexpected() 

### DISK FORMATTING ###
def volumecustomlabel():
    newlabel = states.new_label
    # THIS FUNCTION MUST BE USED AFTER(?) THE DISK IS FORMATTED
    # 1. detect the file type
    fs_type = states.currentFS
    # 2. unmount the drive
    # 3. change the label using the command specific for that file type
    if fs_type==0:
        try:
            subprocess.run(["ntfslabel", drive, newlabel], check=True)
        # except FileNotFoundError:
        #     pkexecNotFound()
        except subprocess.CalledProcessError:
            FormatFail()
        except Exception as e:
            print(f"2. DEBUG: Unexpected error type: {type(e).__name__}")
            print(f"DEBUG: Error message: {e}")
            unexpected()
    elif fs_type==1:
        try:
            subprocess.run(["fatlabel", drive, newlabel], check=True)
        # except FileNotFoundError:
        #     pkexecNotFound()
        except subprocess.CalledProcessError:
            FormatFail()
        except Exception as e:
            print(f"3. DEBUG: Unexpected error type: {type(e).__name__}")
            print(f"DEBUG: Error message: {e}")
            unexpected()
    elif fs_type==2:
        try:
            subprocess.run(["fatlabel", drive, newlabel], check=True)
        # except FileNotFoundError:
        #     pkexecNotFound()
        except subprocess.CalledProcessError:
            FormatFail()
        except Exception as e:
            print(f"4. DEBUG: Unexpected error type: {type(e).__name__}")
            print(f"DEBUG: Error message: {e}")
            unexpected()
    elif fs_type==3:
        try:
            subprocess.run(["e2label", drive, newlabel], check=True)
        # except FileNotFoundError:
        #     pkexecNotFound()
        except subprocess.CalledProcessError:
            FormatFail()
        except Exception as e:
            print(f"5. DEBUG: Unexpected error type: {type(e).__name__}")
            print(f"DEBUG: Error message: {e}")
            unexpected()
    else:
        unexpected()
    # 4. mount the drive again
   

def cluster():
    if not mount_dict:
        print("Error: No USB mount found. Is the drive plugged in and mounted?")
        return None, None, None
    mount = next(iter(mount_dict))  # IMPORT THE INITIAL MOUNT POINT
    drive = fu.find_DN() # IMPORTS DRIVE NODE
    # for physical sector or logical block size
    # NEEDS TROUBLESHOOTING AND ERROR HANDLLING
    try:
        # res1 = subprocess.run(["pkexec", "blockdev", "--getbsz", drive], capture_output=True, text=True, check=True)
        # cluster1 = int(res1.stdout.strip())
        if states.cluster_size == 0:
            cluster1 = 4096
        elif states.cluster_size == 1:
            cluster1 = 8192
        else:
            print("wtf is the cluster size bro?")
    # except FileNotFoundError:
    #     pkexecNotFound()
    except subprocess.CalledProcessError:
        FormatFail()
    except Exception as e:
        print(f"7. DEBUG: Unexpected error type: {type(e).__name__}")
        print(f"DEBUG: Error message: {e}")
        unexpected()  
    # for logical sector size
    try:
        # res2 = subprocess.run(["pkexec", "blockdev", "--getss", drive], capture_output=True, text=True, check=True)
        # cluster2 = int(res2.stdout.strip())
        cluster2 = 512
    # except FileNotFoundError:
    #     pkexecNotFound()
    except subprocess.CalledProcessError:
        FormatFail()
    except Exception as e:
        print(f"8. DEBUG: Unexpected error type: {type(e).__name__}")
        print(f"DEBUG: Error message: {e}")
        unexpected()  
    # convert to sectors
    sector = cluster1//cluster2
    return cluster1, cluster2, sector
    

def quickformat():
    # detect quick format option ticked or not and put it in a variable
    # the if logic will be implemented later
    pass

def createextended():
    # detect create extended label and icon files check box and put it in a variable
    pass

def checkdevicebadblock():
    # following may be used?
    # pkexec badblocks -wsv <mountpath>
    # no idea how to use passes tho
    pass

def dskformat():
    cluster1, cluster2, sector = cluster()
    fs_type = states.currentFS
    #These can later be turned to a notification or error box using pyqt
    #THIS WILL ASK FOR PASSWORD NEED TO FETCH PASSWORD so we are using pkexec from polkit to prompt the user for a password. need to figure out a way to use another method or implement this everywhere.
    # instead of FileNotFoundError we can also use shutil(?)
    clusters = cluster1
    sectors = sector
    # UNMOUNT THE DRIVE   
    # START FORMATTING

    if fs_type==0:
        try:
            subprocess.run(["mkfs.ntfs", "-c", str(clusters), "-Q", drive], check=True)
            print("success format to ntfs!")
        # except FileNotFoundError:
        #     pkexecNotFound()
        except subprocess.CalledProcessError:
            FormatFail()
        except Exception as e:
            print(f"10. DEBUG: Unexpected error type: {type(e).__name__}")
            print(f"DEBUG: Error message: {e}")
            unexpected()
    elif fs_type==1:
        try:
            subprocess.run(["mkfs.vfat", "-s", str(sectors), "-F", "32", drive], check=True)
            print("success format to fat32!")
        # except FileNotFoundError:
        #     pkexecNotFound()
        except subprocess.CalledProcessError:
            FormatFail()
        except Exception as e:
            print(f"11. DEBUG: Unexpected error type: {type(e).__name__}")
            print(f"DEBUG: Error message: {e}")
            unexpected()
    elif fs_type==2:
        try:
            subprocess.run(["mkfs.exfat", "-b", str(clusters), drive], check=True)
            print("success format to exFAT!")
        # except FileNotFoundError:
        #     pkexecNotFound()
        except subprocess.CalledProcessError:
            FormatFail()
        except Exception as e:
            print(f"12. DEBUG: Unexpected error type: {type(e).__name__}")
            print(f"DEBUG: Error message: {e}")
            unexpected()
    elif fs_type==3:
        try:
            subprocess.run(["mkfs.ext4", "-b", str(clusters), drive], check=True)
            print("success format to ext4!")
        # except FileNotFoundError:
        #     pkexecNotFound()
        except subprocess.CalledProcessError:
            FormatFail()
        except Exception as e:
            print(f"13. DEBUG: Unexpected error type: {type(e).__name__}")
            print(f"DEBUG: Error message: {e}")
            unexpected()
    else:
        unexpected()
    # REMOUNT

def drive_repair():
    raw_device = drive.rstrip("0123456789")
    cmd = ["sfdisk", raw_device]
    try:
        subprocess.run(["umount", drive], check=True)
        subprocess.run(cmd, input=b",,0c;\n", check=True)
        subprocess.run(["mkfs.vfat", "-F", "32", "-n", "REPAIRED", drive], check=True)
        print("SUCCESSFULLY REPAIRED DRIVE (FAT32)")
    except: # Add different error handling 
        print("COULDN'T REPAIR DRIVE")
