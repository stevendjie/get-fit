$( function() {
    $("label[for='id_name']").append("<span style='color:red; font-weight:800;'>&nbsp;(required)</span>");

    $("input").addClass("form-control");
    $("input[type='checkbox']").removeClass("form-control");

    $("#addGoal input[id='id_name'").attr('placeholder', 'e.g. Bulk (workout day)');
    $("#addGoal input[id='id_calories'").attr('placeholder', '3000');
    $("#addGoal input[id='id_protein'").attr('placeholder', '175');
    $("#addGoal input[id='id_carbohydrates'").attr('placeholder', '350');
    $("#addGoal input[id='id_fats'").attr('placeholder', '150');

    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();

    if(mm==1)
        mm = "January"
    else if (mm==2)
        mm = "February"
    else if (mm==3)
        mm = "March"
    else if (mm==4)
        mm = "April"
    else if (mm==5)
        mm = "May"
    else if (mm==6)
        mm = "June"
    else if (mm==7)
        mm = "July"
    else if (mm==8)
        mm = "August"
    else if (mm==9)
        mm = "September"
    else if (mm==10)
        mm = "October"
    else if (mm==11)
        mm = "November"
    else if (mm==12)
        mm = "December"
    var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    var day = days[ today.getDay() ];
    today = day + ', ' + dd + ' ' + mm + ' ' + yyyy;
    $(".date").text(today);

    $(".btn-more").on("click", function() {
        var $this = $(this);
		var $i = $this.find($("i"));
        if ($i.hasClass("fa-plus")){
            $i.removeClass("fa-plus");
            $i.addClass("fa-minus");
        } else{
            $i.removeClass("fa-minus");
            $i.addClass("fa-plus");
        }
		$this.parent().parent().next().slideToggle();

	});

})