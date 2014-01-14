
//选中全选按钮，下面的checkbox全部选中
function selectAll()
{
  var obj = document.getElementsByName("case");
  if(document.getElementById("selectall").checked == false)
  {
  for(var i=0; i<obj.length; i++)
  {
    obj[i].checked=false;
  }
  }else
  {
  for(var i=0; i<obj.length; i++)
  {  
    obj[i].checked=true;
  }
  }
 
} 



function setSelectAll()
{
var obj=document.getElementsByName("case");
var count = obj.length;
var selectCount = 0;

for(var i = 0; i < count; i++)
{
if(obj[i].checked == true)
{
selectCount++;
}
}
if(count == selectCount)
{
document.getElementById("selectall").checked  = true;
}
else
{
document.getElementById("selectall").checked  = false;
}
} 




function selectcodeAll()
{
  var obj = document.getElementsByName("code");
  if(document.getElementById("selectcodeall").checked == false)
  {
  for(var i=0; i<obj.length; i++)
  {
    obj[i].checked=false;
  }
  }else
  {
  for(var i=0; i<obj.length; i++)
  {  
    obj[i].checked=true;
  }
  }
 
} 



function setSelectCodeAll()
{
var obj=document.getElementsByName("code");
var count = obj.length;
var selectCount = 0;

for(var i = 0; i < count; i++)
{
if(obj[i].checked == true)
{
selectCount++;
}
}
if(count == selectCount)
{
document.getElementById("selectcodeall").checked  = true;
}
else
{
document.getElementById("selectcodeall").checked  = false;
}
} 

function clearall()
{

  if (document.getElementById("selectcodeall").checked == true)
  {
    document.getElementById("selectcodeall").checked  = false
  }

  if (document.getElementById("selectall").checked == true)
  {
    document.getElementById("selectall").checked  = false
  }
  var code = document.getElementsByName("code");
  for(var i=0; i<code.length; i++)
  {
    code[i].checked=false;
  }

  var case1 = document.getElementsByName("case");
  for(var i=0; i<case1.length; i++)
  {
    case1[i].checked=false;
  }
}