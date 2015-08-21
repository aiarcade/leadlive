define(function(){  
   return {
      greeting: function() {
         var hour = new Date().getHours();
         if (hour < 12) { return "Good morning."; }
         else if (hour < 16) { return "Good afternoon."; }
         else { return "Good evening."; }
      }
   }
});
