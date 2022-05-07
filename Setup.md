# Setup

* Download macOS VM

	1. Download the VM from https://transfer.ttyusb.dev/1YD1PQVF8SYowCMOWE2s2OcuEgKEUQMcA/macOS%20VM.7z
	2. Additional mirror at https://cyberthon2022.sgp1.digitaloceanspaces.com/Finals/macOS%20VM.7z

* To boot up macOS VM
	1. Extract the VM from "macOS VM.7z" using 7zip.
	2. Import the VM into VM Player by selecting "Player" followed by "Open" and select "macOS VM.vmx" in the extracted folder.
	3. Do the following steps if you encounter issues when trying to start up the macOS VM.

		i) Visit https://github.com/paolo-projects/unlocker/releases/download/3.0.4/unlocker.zip to download unlocker (may be required to boot up macOS VM).
		ii) Extract the content of "unlocker.zip" into a folder.
		iii) Copy/move the entire folder into the directory you have installed your VMWare Player. (default is C:/Pogram Files (x86))
		iv) Go inside the folder and right click on "win-install" and click "Run as administrator".
		v) After the installation you should be able to boot up the macOS VM without anymore issues.

	4. Once the VM starts up login using the password "password".

* To install and run the app on the Simulator APP, you will need to run the following commands on the MacOS terminal.
	1. Download the challenge, "Raiden.zip" and extract the content onto the macOS VM.
	2. To open up a terminal, press the windows key + space. A "Spotlight search" prompt will appear type in "terminal" and press enter.
	3. A terminal will appear. Type the following command
		i) xcrun simctl list | grep "iPhone 11"
	4. You will see a line that is similar to this "iPhone 11 (XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX) (Shutdown)"
	5. Copy the XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX portion and run this command: xcrun simctl boot XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
	6. Open up the Simulator App by running: open /Applications/Xcode.app/Contents/Developer/Applications/Simulator.app
	7. You can either drag and drop the Raiden.app file onto the simulator or run (replace <path_to_raiden.app> with actual file path to Raiden.app: xcrun simctl install XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX <path_to_raiden.app>
