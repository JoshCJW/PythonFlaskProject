$(document).ready(function() {
 $("#cform").submit(function(event) {
    event.preventDefault();
    var dateControl = document.querySelector('input[type="date"]');
    var when = dateControl.value;
    var who = document.getElementById("itxtwho").value;
    var comment = document.getElementById("itxtcomment").value;
    var about = document.getElementById("itxtabout").value;
    var media = document.getElementById("itxtmedia").value;
    var what = document.getElementById("itxtwhat").value;
    var whom = document.getElementById("itxtwhom").value;
    var refid = document.getElementById("itxtrefid").value;

    $.post("/catalog",{'when':when,'who':who,'comment':comment,'about':about,'media':media,'what':what,'whom':whom,'refid':refid})
    
    // Get Count data
    var _data;
    var _labels;
    $.ajax({
    url: "/data",
    type: "get",
    data: {vals: ''},
    success: function(response) {
      full_data = JSON.parse(response.tweets);
      
      _data = full_data['data'];
      _labels = full_data['labels'];
    },
    async:false
  });
  // Put response in dic
  var Cyear = when.toString();
  let Cyeartwo = Cyear.slice(0,4)
  const years = _labels
  const county = _data
  var CcountDict = county.reduce(function(result, field, index) {
    result[years[index]] = field;
    return result
  }, {})
  //  to display out
    var dateControl = document.querySelector('input[type="date"]');
    document.getElementById('display_when').innerHTML = when
    document.getElementById('display_who').innerHTML = who
    document.getElementById('display_comment').innerHTML = comment
    document.getElementById('display_about').innerHTML = about
    document.getElementById('display_media').innerHTML = media
    document.getElementById('display_what').innerHTML = what
    document.getElementById('display_whom').innerHTML = whom
    document.getElementById('display_refid').innerHTML = refid
    document.getElementById('when').innerHTML = Cyeartwo
    document.getElementById('count').innerHTML = CcountDict[Cyeartwo]
    var x = document.getElementById("cform");
    x.style.display = "none";

    var y = document.getElementById("sumtable");
    y.style.display = "block";
 })

});

