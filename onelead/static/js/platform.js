var myLayout;
var leftToolbar;
var rightToolbar;
var leftMenu;
var layout1;
var layout2;
var grid;
var scheduler;

function initApp(path,staff_id) {
	
	// main layout
	myLayout = new dhtmlXLayoutObject({
		parent: document.body,
		pattern: "2U"
	});
	myLayout.cells("a").fixSize(true, true);
	
	// left cell
	layout1 = myLayout.cells("a").attachLayout("1C");
	layout1.cells("a").hideHeader();
	leftToolbar = layout1.attachToolbar({
		icons_path: path,
		icons_size: 48,
		items: [
			{type: "button", img: "folder-image-people.png", title: "Receive Mail", id: "receive"},
			{type: "separator"},
			
		]
	});
	
	leftMenu = layout1.cells("a").attachDataView({
		type: {
			template: "<div class='menu_item #id#'>"+
					"<div class='menu_item_text'>#text#</div>"+
				"</div>",
			margin: 0,
			padding: 0,
			height: 60
		},
		drag: false,
		select: true
	});
	
    //scheduler.config.xml_date="%d/%m/%Y %H:%i";
    //scheduler.config.first_hour=8;
    //scheduler.config.limit_time_select = true;
	//scheduler.config.prevent_cache = true;
    //scheduler.config.edit_on_create = true;
	//scheduler.config.collision_limit = 1;
    //scheduler.config.details_on_create=true;
    //scheduler.config.details_on_dblclick = true;
    //scheduler.config.max_month_events = 10;
    //scheduler.init('timetable');
    
    
    
    
	leftMenu.parse([
		{id: "attendance", img: "folder-image-people.png", text: "Attendance"},
		
	], "json");
	
    
   
    
	leftMenu.attachEvent("onSelectChange", function(id) {
		if (grid == null) { // first init
    
    
        //layout2.cells("a").setWidth(800);
         
        scheduler = layout2.cells("a").attachScheduler();
        scheduler.config.xml_date="%d/%m/%Y %H:%i";
		scheduler.config.first_hour=6;
		scheduler.config.limit_time_select = true;
		scheduler.config.prevent_cache = true;
        scheduler.config.edit_on_create = true;
		scheduler.config.collision_limit = 1;
        scheduler.config.details_on_create=true;
        scheduler.config.details_on_dblclick = true;
        scheduler.config.max_month_events = 10;
        
        
        
		scheduler.load('/platform/ajax/?staffid='+staff_id,"json");
		} else {
			//grid.clearAll(true);
		}		
		
		
	});
	
	// right cell
	layout2 = myLayout.cells("b").attachLayout("1C");
	layout2.cells("a").hideHeader();
	
	rightToolbar = layout2.attachToolbar({
		icons_path: path,
		icons_size: 48,
		items: [
			{type: "button", img: "folder-image-people.png", title: "New Mail", id: "new_mail"},
			{type: "separator"},
			
		]
	});
	
	function getLeftColumnWidth() {
		if ( navigator.platform.match(/(Mac|iPhone|iPod|iPad)/i) ) {
			return Math.round(document.body.offsetWidth*0.25);
		} else {
			return Math.max(document.body.offsetWidth*0.12, 250);
		}
	}
	
	function hide_show_toolbar_items() {
		if (window.orientation == 0 || window.orientation == 180) {	//"portrait"
			leftToolbar.hideItem("print");
			leftToolbar.hideItem("settings");
			rightToolbar.hideItem("dialog_inf");
			rightToolbar.hideItem("contact");
			rightToolbar.hideItem("help");
		} else {	//"landscape"
			leftToolbar.showItem("print");
			leftToolbar.showItem("settings");
			rightToolbar.showItem("dialog_inf");
			rightToolbar.showItem("contact");
			rightToolbar.showItem("help");
		}
	}
		
	function change_leftMenu_width_by_orientation() {
		myLayout.cells("a").setWidth(getLeftColumnWidth());		
		leftMenu.define("type",{
				width:(myLayout.cells("a").getWidth() - 5) // ( getLeftColumnWidth() - 5 )
		});
		hide_show_toolbar_items();
	}
		
	if (typeof(window.addEventListener) == "function") {
		window.addEventListener("orientationchange", function(e){
			change_leftMenu_width_by_orientation();
		});
		
		window.addEventListener("resize", function(e){
			change_leftMenu_width_by_orientation();
		});
	} else {
		window.attachEvent("onorientationchange", function(e){
			change_leftMenu_width_by_orientation();
		});
		
		window.attachEvent("onresize", function(e){
			change_leftMenu_width_by_orientation();
		});
	}
		
	change_leftMenu_width_by_orientation();	
	leftMenu.select("attendance");	
}
