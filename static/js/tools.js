function deleteuser( user ) {

  Check = confirm("Do you really want to delete "+user+"?");
  
  if (Check == true) { 
      $.post("../admin/delete.php", {delete: user}); 
      $.ajax({
			type:    'POST',
			url :    "../admin/delete.php",
			data:    { delete: user },
			success: function (data) {
		      window.location.reload();
			} });
      //return true; 
  }
   
}

function setrightsnew( user, admin, repo ) {

  if (admin) {
      $.post("../admin/rights.php", {user: user, admin: "true", repo: "true", newuser: "true"});  
  } else if (repo) {
      $.post("../admin/rights.php", {user: user, repo: "true", newuser: "true"});
  } else {
      $.post("../admin/rights.php", {user: user, newuser: "true"});   
  }
}

function setrights( user, admin, repo ) {

  if (admin) {
      $.post("../admin/rights.php", {user: user, admin: "true", repo: "true"});  
  } else if (repo) {
      $.post("../admin/rights.php", {user: user, repo: "true"});
  } else {
      $.post("../admin/rights.php", {user: user});   
  }
}

function showinfo( details ) {

  $(this).click(function() {
    $(".userinfo").toggle();
  });
}
