########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinndesign.com
########################################################################

########################################################################
## IMPORTS
########################################################################
import sys
import os
# pip install pyside2
from PySide2 import *
# pip install psutil
import psutil
from multiprocessing import cpu_count
import datetime
# pip install qt_material
from qt_material import *
import shutil 
import platform
# pip install qt_material
import PySide2extn
from time import time, sleep
########################################################################

########################################################################
# IMPORT GUI FILE
from ui_interface import *
########################################################################

########################################################################
# GOBAL
platforms = {
'linux' : 'Linux',
'linux1' : 'Linux',
'linux2' : 'Linux',
'darwin' : 'OS X',
'win32' : 'Windows'
}
########################################################################


########################################################################
## WORKER SIGNAL CLASS
########################################################################
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

########################################################################
## 
########################################################################


########################################################################
## WORKER  CLASS
########################################################################
class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


########################################################################
## 
########################################################################


########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):# setup stylesheet
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #######################################################################
        # # Load Style sheet , this will overide and fonts selected in qt designer
        ######################################################################## 
        apply_stylesheet(app, theme='dark_cyan.xml')

        #######################################################################
        ## # Remove window tlttle bar
        ########################################################################    
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) 

        #######################################################################
        ## # Set main background to transparent
        ########################################################################  
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
      
        #######################################################################
        ## # Shadow effect style
        ########################################################################  
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))
        
        #######################################################################
        ## # Appy shadow to central widget
        ########################################################################  
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        #######################################################################
        # Set window Icon
        # This icon and title will not appear on our app main window because we removed the title bar
        #######################################################################
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/feather/airplay.svg"))
        # Set window tittle
        self.setWindowTitle("UTIL Manager")

        #################################################################################
        # Window Size grip to resize window
        #################################################################################
        QSizeGrip(self.ui.size_grip)

        #######################################################################
        #Minimize window
        self.ui.minimizeWindowButton.clicked.connect(lambda: self.showMinimized())
        #######################################################################
        #Close window
        self.ui.closeWindowButton.clicked.connect(lambda: self.close())
        #######################################################################
        #Restore/Maximize window
        self.ui.restoreWindowButton.clicked.connect(lambda: self.restore_or_maximize_window())


        #######################################################################
        # STACKED PAGES NAVIGATION/////////////////
        #Using side menu buttons
        #######################################################################

        #navigate to CPU page
        self.ui.cpu_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_page))        

        #navigate to Battery page
        self.ui.battery_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.battery_info))
        
        #navigate to System Inf page
        self.ui.system_inf_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.system_info))

        #navigate to Activity page
        self.ui.activity_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.activities))

        #navigate to Storage page
        self.ui.storage_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.storage))

        #navigate to Sensors page
        self.ui.sensors_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sensors))

        #navigate to Sensors page
        self.ui.networks_page_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.network))
        #######################################################################



        # ###############################################
        # Function to Move window on mouse drag event on the tittle bar
        # ###############################################
        def moveWindow(e):
            # Detect if the window is  normal size
            # ###############################################  
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size  
                # ###############################################
                #if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:  
                    #Move window 
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        #######################################################################

        
        #######################################################################
        # Add click event/Mouse move event/drag event to the top header to move the window
        #######################################################################
        self.ui.header_frame.mouseMoveEvent = moveWindow
        #######################################################################

        #######################################################################
        #Left Menu toggle button (Show hide menu labels)
        self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())

        #######################################################################
        # Style clicked menu button
        for w in self.ui.left_side_menu.findChildren(QPushButton):
            # Add click event listener
            w.clicked.connect(self.applyButtonStyle)
        #######################################################################


        #######################################################################
        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## == #
        #######################################################################

        #######################################################################
        # START THREAD
        self.threadpool = QThreadPool()
        #######################################################################

        #######################################################################
        # FUNCTIONS
        #######################################################################
        # self.battery()
        self.psutil_thread()
        self.system_info()
        self.processes()
        self.storage()
        self.sensors()
        self.networks()
        #######################################################################
        # 
        #######################################################################


    ########################################################################
    ## CREATE PSUTIL THREAD FUNCTION 
    ########################################################################
    def psutil_thread(self):
        worker = Worker(self.cpu_ram)

        # START WORKER
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

        battery_worker = Worker(self.battery)

        # START WORKER
        battery_worker.signals.result.connect(self.print_output)
        battery_worker.signals.finished.connect(self.thread_complete)
        battery_worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(battery_worker)

    ########################################################################
    ## 
    ########################################################################



    ########################################################################
    ## WORKER PRINT OUT
    ########################################################################
    def print_output(self, s):
        print(s)
    ########################################################################
    ## 
    ########################################################################

    ########################################################################
    ## WORKER THREAD COMPLETE FUNCTION
    ########################################################################
    def thread_complete(self):
        print("THREAD COMPLETE!")
    ########################################################################
    ## 
    ########################################################################



    ########################################################################
    ## WORKER THREAD PROGRESS FUNCTION
    ########################################################################
    def progress_fn(self, n):
        # n = progress value
        print("%d%% done" % n)
    ########################################################################
    ## 
    ########################################################################



    ########################################################################
    # Start Menu buttons styling function
    ########################################################################
    def applyButtonStyle(self):
        # Reset style for other buttons
        for w in self.ui.left_side_menu.findChildren(QPushButton):
            # If the button name is not equal to clicked button name
            if w.objectName() != self.sender().objectName():
                # Create default style by removing the left border
                # Lets remove the bottom border style

                # Lets also remove the left border style

                # Apply the default style
                w.setStyleSheet("border-bottom: none;")
                #                 

        # Apply new style to clicked button
        # Sender = clicked button
        # Get the clicked button stylesheet then add new left-border style to it
        # Lets add the bottom border style
        # Apply the new style
        self.sender().setStyleSheet("border-bottom: 2px solid")
        # 
        return
    #######################################################################

    #######################################################################
    # Add mouse events to the window
    #######################################################################
    def mousePressEvent(self, event):
        # ###############################################
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to move the window
    #######################################################################
    #######################################################################

    #######################################################################
    # Update restore button icon on msximizing or minimizing window
    #######################################################################
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.restoreWindowButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-restore.png"))
        else:
            self.showMaximized()
            self.ui.restoreWindowButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-maximize.png"))


    ########################################################################
    # Slide left menu function
    ########################################################################
    def slideLeftMenu(self):
        # Get current left menu width
        width = self.ui.side_menu_frame.width()

        # If minimized
        if width == 40:
            # Expand menu
            newWidth = 200
        # If maximized
        else:
            # Restore menu
            newWidth = 40

        # Animate the transition
        self.animation = QPropertyAnimation(self.ui.side_menu_frame, b"minimumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
    #######################################################################

    #######################################################################
    # Get sytem battery information
    #######################################################################
    def battery(self, progress_callback):
        while True:
            batt = psutil.sensors_battery()

            if not hasattr(psutil, "sensors_battery"):
                self.ui.battery_status.setText("Platform not supported")

            if batt is None:
                self.ui.battery_status.setText("No battery installed")

            if batt.power_plugged:
                self.ui.battery_charge.setText(str(round(batt.percent, 2))+"%")
                self.ui.battery_time_left.setText("N/A")
                if batt.percent < 100:
                    self.ui.battery_status.setText("Charging")
                else:
                    self.ui.battery_status.setText("Fully Charged")  

                self.ui.battery_plugged.setText("Yes")

            else:
                self.ui.battery_charge.setText(str(round(batt.percent, 2))+"%")
                self.ui.battery_time_left.setText(self.secs2hours(batt.secsleft))
                if batt.percent < 100:
                    self.ui.battery_status.setText("Discharging")
                else:
                    self.ui.battery_status.setText("Fully Charged")         
                self.ui.battery_plugged.setText("No")

            # BATTERY POWER INDICATOR USING ROUND PROGRESS BAR
            # SET PROGRESS BAR VALUE
            self.ui.battery_usage.rpb_setMaximum(100) 
            # Set progress values
            self.ui.battery_usage.rpb_setValue(batt.percent)
            # SET PROGRESS BAR STYLE
            self.ui.battery_usage.rpb_setBarStyle('Hybrid2')
            # SET PROGRESS BAR LINE COLOR
            self.ui.battery_usage.rpb_setLineColor((255, 30, 99)) 
            # SET PROGRESS BAR LINE COLOR
            # self.ui.battery_usage.rpb_setCircleColor((45, 74, 83)) 
            # SET PROGRESS BAR LINE COLOR
            self.ui.battery_usage.rpb_setPieColor((45, 74, 83)) 
            #CHANGING THE PATH COLOR
            # self.ui.battery_usage.rpb_setPathColor((45, 74, 83))
            #SET PROGRESS BAR TEXT COLOR
            self.ui.battery_usage.rpb_setTextColor((255, 255, 255))
            # SET PROGRESS BAR STARTING POSITION
            # North, East, West, South
            self.ui.battery_usage.rpb_setInitialPos('West') 
            #SET PROGRESS BAR TEXT TYPE : VALUE OR PERCENTAGE
            # Value, Percentage
            self.ui.battery_usage.rpb_setTextFormat('Percentage')
            #SET PROGRESS BAR FONT
            #SET PROGRESS BAR LINE WIDTH 
            self.ui.battery_usage.rpb_setLineWidth(15)
            #PATH WIDTH
            self.ui.battery_usage.rpb_setPathWidth(15)
            #SET PROGRESS BAR LINE CAP
            # RoundCap, SquareCap
            self.ui.battery_usage.rpb_setLineCap('RoundCap')
            #LINE STYLE
            # DotLine, DashLine
            # self.ui.battery_usage.rpb_setLineStyle('DotLine')
            # SLEEP FOR 1 SEC
            sleep(1)


    #######################################################################
    # A function to convert seconds to hours
    #######################################################################
    def secs2hours(self, secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d (H:M:S)" % (hh, mm, ss)
    #######################################################################
    #######################################################################

    #######################################################################
    # System CPU and Ram information
    #######################################################################
    def cpu_ram(self, progress_callback):
        while True:
            totalRam = 1.0
            totalRam = psutil.virtual_memory()[0] * totalRam
            totalRam = totalRam / (1024 * 1024 * 1024)
            self.ui.total_ram.setText(str("{:.4f}".format(totalRam) + ' GB'))

            availRam = 1.0
            availRam = psutil.virtual_memory()[1] * availRam
            availRam = availRam / (1024 * 1024 * 1024)
            self.ui.available_ram.setText(str("{:.4f}".format(availRam) + ' GB'))


            ramUsed = 1.0
            ramUsed = psutil.virtual_memory()[3] * ramUsed
            ramUsed = ramUsed / (1024 * 1024 * 1024)
            self.ui.used_ram.setText(str("{:.4f}".format(ramUsed) + ' GB'))

            ramFree = 1.0
            ramFree = psutil.virtual_memory()[4] * ramFree
            ramFree = ramFree / (1024 * 1024 * 1024)
            self.ui.free_ram.setText(str("{:.4f}".format(ramFree) + ' GB'))

            core = cpu_count()
            self.ui.cpu_count.setText(str(core))

            ramUsages = str(psutil.virtual_memory()[2]) + '%'
            self.ui.ram_usage.setText(str("{:.4f}".format(totalRam) + ' GB'))

            cpuPer = psutil.cpu_percent()
            self.ui.cpu_per.setText(str(cpuPer) + " %")

            cpuMainCore = psutil.cpu_count(logical=False)
            self.ui.cpu_main_core.setText(str(cpuMainCore))

            # CPU PERCENTAGE INDICATOR
            # SET PROGRESS BAR VALUE
            self.ui.cpu_percentage.rpb_setMaximum(100) 
            # Set progress values
            self.ui.cpu_percentage.rpb_setValue(cpuPer)
            # SET PROGRESS BAR STYLE
            self.ui.cpu_percentage.rpb_setBarStyle('Hybrid2')
            # SET PROGRESS BAR LINE COLOR
            self.ui.cpu_percentage.rpb_setLineColor((255, 30, 99))
            # SET PROGRESS BAR LINE COLOR
            # self.ui.cpu_percentage.rpb_setCircleColor((45, 74, 83))
            # SET PROGRESS BAR LINE COLOR
            self.ui.cpu_percentage.rpb_setPieColor((45, 74, 83))
            #CHANGING THE PATH COLOR
            # self.ui.cpu_percentage.rpb_setPathColor((45, 74, 83))
            #SET PROGRESS BAR TEXT COLOR
            self.ui.cpu_percentage.rpb_setTextColor((255, 255, 255)) 
            # SET PROGRESS BAR STARTING POSITION
            # North, East, West, South
            self.ui.cpu_percentage.rpb_setInitialPos('West')
            #SET PROGRESS BAR TEXT TYPE : VALUE OR PERCENTAGE
            # Value, Percentage
            self.ui.cpu_percentage.rpb_setTextFormat('Percentage')

            #SET PROGRESS BAR FONT
            self.ui.cpu_percentage.rpb_setTextFont('Arial')        
            #TEXT HIDDEN
            # self.ui.cpu_percentage.rpb_enableText(False) 
            #SET PROGRESS BAR LINE WIDTH 
            self.ui.cpu_percentage.rpb_setLineWidth(15)
            #PATH WIDTH
            self.ui.cpu_percentage.rpb_setPathWidth(15)
            #SET PROGRESS BAR LINE CAP
            # RoundCap, SquareCap
            self.ui.cpu_percentage.rpb_setLineCap('RoundCap')
            #LINE STYLE
            # DotLine, DashLine
            # self.ui.cpu_percentage.rpb_setLineStyle('DotLine')

            # RAM USAGE INDICATOR USING SPIRAL PROGRESSBAR
            # #######################################################################
            # #SETTING THE MINIMUM VALUE
            self.ui.ram_percantage.spb_setMinimum((0, 0, 0))
            # #######################################################################
            # #######################################################################
            # #SETTING THE MAXIMUM VALUE
            self.ui.ram_percantage.spb_setMaximum((totalRam, totalRam, totalRam))  
            # #######################################################################
            # #######################################################################
            # # SET PROGRESS VALUE
            self.ui.ram_percantage.spb_setValue((availRam, ramUsed, ramFree))
            # #######################################################################
            # #######################################################################
            # #SET PROGRESS COLOR (R, G, B)
            self.ui.ram_percantage.spb_lineColor(((6,233,38), (6,201,233), (233,6,201)))
            # #######################################################################
            # #######################################################################
            # #SETING THE INITIAL POSITION OF THE PROGRESS BAR: FROM OUTER->INWARDS
            self.ui.ram_percantage.spb_setInitialPos(('West', 'West', 'West'))
            # #######################################################################
            # #######################################################################
            # #SETING THE DIRECTION OF PROGRESS OF THE PROGRESS BAR: FROM OUTER-INWARDS
            # self.ui.ram_percantage.spb_setDirection(('Clockwise', 'AntiClockwise', 'Clockwise'))
            # #######################################################################
            # #######################################################################
            # #SET LINE WIDTH: 15px
            self.ui.ram_percantage.spb_lineWidth(15)
            # #######################################################################
            # #######################################################################
            # #SET GAP WIDTH
            self.ui.ram_percantage.spb_setGap(15)
            # #######################################################################
            # #######################################################################
            # #SET LINE STYLE
            self.ui.ram_percantage.spb_lineStyle(('SolidLine', 'SolidLine', 'SolidLine'))
            # #######################################################################
            # #######################################################################
            # #SET LINE CAP
            self.ui.ram_percantage.spb_lineCap(('RoundCap', 'RoundCap', 'RoundCap'))
            # #######################################################################
            # #######################################################################
            # #HIDE THE PATH
            self.ui.ram_percantage.spb_setPathHidden(True)
            # #######################################################################
            # SLEEP FOR 1 SEC
            sleep(1)


    #######################################################################
    # GET SYSTEM INFORMATION
    #######################################################################
    def system_info(self):
        time = datetime.datetime.now().strftime("%I:%M:%S %p")
        self.ui.system_date.setText(str(time))  
        date = datetime.datetime.now().strftime("%Y-%m-%d")          
        self.ui.system_time.setText(str(date))

        
        self.ui.system_machine.setText(platform.machine())
        self.ui.system_version.setText(platform.version())
        self.ui.system_platform.setText(platform.platform())
        self.ui.system_sytem.setText(platform.system())
        self.ui.system_processor.setText(platform.processor())
    #######################################################################

    #######################################################################
    # RUNNING PROCESSES
    #######################################################################
    def processes(self):
        for x in psutil.pids():
            # Create New Row
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)

            try:        
                process = psutil.Process(x)
                # # Create widget
                # print(process)
                # # rowPosition = row number
                # # x = column number
                    

                self.create_table_widget(rowPosition, 0, str(process.pid), "tableWidget")
                self.create_table_widget(rowPosition, 1, process.name(), "tableWidget")
                self.create_table_widget(rowPosition, 2, process.status(), "tableWidget")
                self.create_table_widget(rowPosition, 3, str(datetime.datetime.utcfromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')), "tableWidget")

                # create an cell widget
                suspend_btn = QPushButton(self.ui.tableWidget)
                suspend_btn.setText('Suspend')
                suspend_btn.setStyleSheet("color: brown")
                self.ui.tableWidget.setCellWidget(rowPosition, 4, suspend_btn)

                resume_btn = QPushButton(self.ui.tableWidget)
                resume_btn.setText('Resume')
                resume_btn.setStyleSheet("color: green")
                self.ui.tableWidget.setCellWidget(rowPosition, 5, resume_btn)

                terminate_btn = QPushButton(self.ui.tableWidget)
                terminate_btn.setText('Terminate')
                terminate_btn.setStyleSheet("color: orange")
                self.ui.tableWidget.setCellWidget(rowPosition, 6, terminate_btn)

                kill_btn = QPushButton(self.ui.tableWidget)
                kill_btn.setText('Kill')
                kill_btn.setStyleSheet("color: red")
                self.ui.tableWidget.setCellWidget(rowPosition, 7, kill_btn)
            except Exception as e:
                print(e)

        # print(self.ui.tableWidget.findItems("sleeping", QtCore.Qt.MatchFlag.MatchRecursive|QtCore.Qt.MatchFlag.MatchExactly))
        self.ui.activity_search.textChanged.connect(self.findName)

        # 
        # ADD YOUR OWN FUNCTION TO SEARCH/FILTER TABLE
        # 

    def findName(self):
        name = self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(row, 1)
            # if the search is *not* in the item's text *do not hide* the row
            self.ui.tableWidget.setRowHidden(row, name not in item.text().lower())

    #######################################################################
    # STORAGE PARTITIONS
    #######################################################################
    def storage(self):
        storage_device = psutil.disk_partitions(all=False)
        z = 0
        for x in storage_device:
            # print(x)
            # Create New Row
            rowPosition = self.ui.storageTable.rowCount()
            self.ui.storageTable.insertRow(rowPosition)

            self.create_table_widget(rowPosition, 0, x.device, "storageTable")
            self.create_table_widget(rowPosition, 1, x.mountpoint, "storageTable")
            self.create_table_widget(rowPosition, 2, x.fstype, "storageTable")
            self.create_table_widget(rowPosition, 3, x.opts, "storageTable")

            if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform == 'linux2':
                self.create_table_widget(rowPosition, 4, str(x.maxfile), "storageTable")
                self.create_table_widget(rowPosition, 5, str(x.maxpath), "storageTable")
            else:
                self.create_table_widget(rowPosition, 4, "Function not available on " + platforms[sys.platform], "storageTable")
                self.create_table_widget(rowPosition, 5, "Function not available on " + platforms[sys.platform], "storageTable")

            # print(psutil.disk_usage(x.device))
            disk_usage = shutil.disk_usage(x.mountpoint)
            # print(disk_usage.total)
            self.create_table_widget(rowPosition, 6, str((disk_usage.total / (1024 * 1024 * 1024))) + " GB", "storageTable")
            self.create_table_widget(rowPosition, 7, str((disk_usage.free / (1024 * 1024 * 1024))) + " GB", "storageTable")
            self.create_table_widget(rowPosition, 8, str((disk_usage.used / (1024 * 1024 * 1024))) + " GB", "storageTable")
            # print(shutil.disk_usage(x.mountpoint))

            full_disk = (disk_usage.used / disk_usage.total) * 100
            progressBar = QProgressBar(self.ui.storageTable)
            progressBar.setObjectName(u"progressBar")
            progressBar.setValue(full_disk)
            self.ui.storageTable.setCellWidget(rowPosition, 9, progressBar)
    #######################################################################

    #######################################################################
    # SENSORS INFORMATION
    #######################################################################
    def sensors(self):
        # PSUTIL Sensors urrently only works on linux platform
        if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform == 'linux2':           
            for x in psutil.sensors_temperatures():
                for y in psutil.sensors_temperatures()[x]:
                    # Create New Row
                    rowPosition = self.ui.sensorTable.rowCount()
                    self.ui.sensorTable.insertRow(rowPosition)

                    self.create_table_widget(rowPosition, 0, x, "sensorTable")
                    self.create_table_widget(rowPosition, 1, y.label, "sensorTable")
                    self.create_table_widget(rowPosition, 2, str(y.current), "sensorTable")
                    self.create_table_widget(rowPosition, 3, str(y.high), "sensorTable")
                    self.create_table_widget(rowPosition, 4, str(y.critical), "sensorTable")

                    temp_per = (y.current / y.high) * 100

                    progressBar = QProgressBar(self.ui.sensorTable)
                    progressBar.setObjectName(u"progressBar")
                    progressBar.setValue(temp_per)
                    self.ui.sensorTable.setCellWidget(rowPosition, 5, progressBar)
        else:
            global platforms
            # Create New Row
            rowPosition = self.ui.sensorTable.rowCount()
            self.ui.sensorTable.insertRow(rowPosition)

            self.create_table_widget(rowPosition, 0, "Function not supported on " + platforms[sys.platform], "sensorTable")
            self.create_table_widget(rowPosition, 1, "N/A", "sensorTable")
            self.create_table_widget(rowPosition, 2, "N/A", "sensorTable")
            self.create_table_widget(rowPosition, 3, "N/A", "sensorTable")
            self.create_table_widget(rowPosition, 4, "N/A", "sensorTable")
            self.create_table_widget(rowPosition, 5, "N/A", "sensorTable")
    #######################################################################

    #######################################################################
    # A FUNCTION THAT CREATES TABLE WIDGETS
    #######################################################################
    def create_table_widget(self, rowPosition, columnPosition, text, tableName):
        qtablewidgetitem = QTableWidgetItem()
        # USE getattr() METHOD
        getattr(self.ui, tableName).setItem(rowPosition, columnPosition, qtablewidgetitem)
        qtablewidgetitem = getattr(self.ui, tableName).item(rowPosition, columnPosition)

        qtablewidgetitem.setText(text);
    #######################################################################
    #######################################################################

    #######################################################################
    # NETWORKS FUNCTIONS 
    #######################################################################
    def networks(self):
        # NET STATS
        for x in psutil.net_if_stats():
            z = psutil.net_if_stats()
            # Create New Row
            rowPosition = self.ui.net_stats_table.rowCount()
            self.ui.net_stats_table.insertRow(rowPosition)

            self.create_table_widget(rowPosition, 0, x, "net_stats_table")
            self.create_table_widget(rowPosition, 1, str(z[x].isup), "net_stats_table")
            self.create_table_widget(rowPosition, 2, str(z[x].duplex), "net_stats_table")
            self.create_table_widget(rowPosition, 3, str(z[x].speed), "net_stats_table")
            self.create_table_widget(rowPosition, 4, str(z[x].mtu), "net_stats_table")

        # NET IO COUNTERS
        for x in psutil.net_io_counters(pernic=True):
            z = psutil.net_io_counters(pernic=True)
            # Create New Row
            rowPosition = self.ui.net_io_table.rowCount()
            self.ui.net_io_table.insertRow(rowPosition)

            self.create_table_widget(rowPosition, 0, x, "net_io_table")
            self.create_table_widget(rowPosition, 1, str(z[x].bytes_sent), "net_io_table")
            self.create_table_widget(rowPosition, 2, str(z[x].bytes_recv), "net_io_table")
            self.create_table_widget(rowPosition, 3, str(z[x].packets_sent), "net_io_table")
            self.create_table_widget(rowPosition, 4, str(z[x].packets_recv), "net_io_table")
            self.create_table_widget(rowPosition, 5, str(z[x].errin), "net_io_table")
            self.create_table_widget(rowPosition, 6, str(z[x].errout), "net_io_table")
            self.create_table_widget(rowPosition, 7, str(z[x].dropin), "net_io_table")
            self.create_table_widget(rowPosition, 8, str(z[x].dropout), "net_io_table")

        # NET ADDRESSES
        for x in psutil.net_if_addrs():
            z = psutil.net_if_addrs()
            # print(z)
            for y in z[x]:  
                # Create New Row
                rowPosition = self.ui.net_addresses_table.rowCount()
                self.ui.net_addresses_table.insertRow(rowPosition)

                self.create_table_widget(rowPosition, 0, str(x), "net_addresses_table")
                self.create_table_widget(rowPosition, 1, str(y.family), "net_addresses_table")
                self.create_table_widget(rowPosition, 2, str(y.address), "net_addresses_table")
                self.create_table_widget(rowPosition, 3, str(y.netmask), "net_addresses_table")
                self.create_table_widget(rowPosition, 4, str(y.broadcast), "net_addresses_table")
                self.create_table_widget(rowPosition, 5, str(y.ptp), "net_addresses_table")

        # NET CONNECTIONS
        for x in psutil.net_connections():
            z = psutil.net_connections()
            # Create New Row
            rowPosition = self.ui.net_connections_table.rowCount()
            self.ui.net_connections_table.insertRow(rowPosition)

            self.create_table_widget(rowPosition, 0, str(x.fd), "net_connections_table")
            self.create_table_widget(rowPosition, 1, str(x.family), "net_connections_table")
            self.create_table_widget(rowPosition, 2, str(x.type), "net_connections_table")
            self.create_table_widget(rowPosition, 3, str(x.laddr), "net_connections_table")
            self.create_table_widget(rowPosition, 4, str(x.raddr), "net_connections_table")
            self.create_table_widget(rowPosition, 5, str(x.status), "net_connections_table")
            self.create_table_widget(rowPosition, 6, str(x.pid), "net_connections_table")
            
            
            
    #######################################################################
    #######################################################################
            

########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################  

#######################################################################
# PATREONS ONLY/ EARLY ACCESS 
#######################################################################
# THANK YOU FOR YOUR SUPPORT
#######################################################################


