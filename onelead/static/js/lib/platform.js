goog.provide('platform');
goog.provide('platform.Attendance');
goog.require('goog.ui.Dialog');
goog.require('goog.events');



platform.Attendance = function(date,hour,batchDivId,staffId) {
    this.date = date;
    this.hour = hour;
    this.batchDivId = batchDivId;
    this.staffId = staffId;
};

platform.Attendance.prototype.setDate = function(date){
    this.date=date;

}

platform.Attendance.prototype.setHour = function(hour){
    this.hour=hour;
}

platform.Attendance.prototype.setStudentList=function(){
    this.studentList = [
    {'Id': 'L66', 'Name': 'Mahesh'},
    {'Id': 'L77', 'Name': 'Raffel'}];
}

platform.Attendance.prototype.createDialogContents=function(){
    
    
    
    }

platform.Attendance.prototype.createDialog=function(){
    
    var dialog1 = new goog.ui.Dialog();
    
    dialog1.setTitle('My favorite LOLCat');

    dialog1.setButtonSet(goog.ui.Dialog.ButtonSet.CONTINUE_SAVE_CANCEL);

    goog.events.listen(dialog1, goog.ui.Dialog.EventType.SELECT, function(e) {
      alert('You chose: ' + e.key);
    });
    dialog1.setVisible(true);
    
    
}
