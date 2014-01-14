
  function addNewCase(test)
 { 

      for (var k=0;k<test.length;k++)
     { 
        if (test =='')
        {alert("请选择用例！");}
        else
        {
        var temp = getalldata('casetable');
        var name = test[k].split('=')[1];
        if (!temp.in_array(name))
        {
            
          //先创建行tr 
        var row = document.createElement("tr"); 
        
        
          //设置行对象的ID属性为用户输入的用户名称 
        row.setAttribute("id",name); 
          //创建td对象 
        column = document.createElement("td"); 
          //td对象下添加子节点 - 内容 TextNode 对象 
        var textrow = document.createElement("input"); 
        textrow.setAttribute("type","text"); 
        textrow.setAttribute("readonly","readonly"); 
        textrow.setAttribute("name","case_test");
        textrow.setAttribute("value",name); 
         //row对象将td对象添加为子节点对象 

        column.appendChild(textrow); 
        row.appendChild(column); 
         //再创建删除按钮 


          var delBtn = document.createElement("input"); 
          //类型 
          delBtn.setAttribute("type","button"); 
          delBtn.setAttribute("class","btn"); 
     
          //文本 
          delBtn.setAttribute("value","删除"); 
          delBtn.setAttribute("onclick","delCase('" + name +"');"); 

     
          //设置对象的事件处理 - 所调用的函数 
          //var name = test[k]; 
          //"delUser(" + test[k] +")"

          //delBtn.onclick= function(){delUser(name);}; 

          column = document.createElement("td"); 
         
          column.appendChild(delBtn); 
                         
          //行对象添加 
          row.appendChild(column); 

          //添加这一行到tbody中 
          document.getElementById('CaseList').appendChild(row); 
      } 
    }
    }
  } 
  //删除元素 
  function delCase(name)

  { 
      if(name!=null)
      { 
          var objRow = document.getElementById(name); 
         var objTBODY = document.getElementById("CaseList"); 
         //删除 
         objTBODY.removeChild(objRow); 
      } 
  } 



    function addNewCode(test)
 { 

      for (var k=0;k<test.length;k++)
     { 
        if (test =='')
        {alert("请选择代码！");}
        else
        {
        var temp = getalldata('codetable');
        var name = test[k].split('=')[1];
        if (!temp.in_array(name))
        {
          //先创建行tr 
        var row = document.createElement("tr"); 
        var name = test[k].split('=')[1];
          //设置行对象的ID属性为用户输入的用户名称 
        row.setAttribute("id",name); 
          //创建td对象 
        column = document.createElement("td"); 
          //td对象下添加子节点 - 内容 TextNode 对象 
        var textrow = document.createElement("input"); 
        textrow.setAttribute("type","text"); 
        textrow.setAttribute("readonly","readonly"); 
        textrow.setAttribute("name","code_test");
        textrow.setAttribute("value",name); 
         //row对象将td对象添加为子节点对象 

        column.appendChild(textrow); 
        row.appendChild(column); 
         //再创建删除按钮 


          var delBtn = document.createElement("input"); 
          //类型 
          delBtn.setAttribute("type","button"); 
          delBtn.setAttribute("class","btn"); 
     
          //文本 
          delBtn.setAttribute("value","删除"); 
          delBtn.setAttribute("onclick","delCode('" + name +"');"); 

     
          //设置对象的事件处理 - 所调用的函数 
          //var name = test[k]; 
          //"delUser(" + test[k] +")"

          //delBtn.onclick= function(){delUser(name);}; 

          column = document.createElement("td"); 
         
          column.appendChild(delBtn); 
                         
          //行对象添加 
          row.appendChild(column); 

          //添加这一行到tbody中 
          document.getElementById('CodeList').appendChild(row); 
      } 
    }
    }
  } 
  //删除元素 
  function delCode(name)

  { 
      if(name!=null)
      { 
          var objRow = document.getElementById(name); 
         var objTBODY = document.getElementById("CodeList"); 
         //删除 
         objTBODY.removeChild(objRow); 
      } 
  } 



function getalldata(name)
{
var tb=document.getElementById(name);
var arrData=new Array();
for(var k=0;k<tb.rows.length;k++){
   arrData[k] = tb.rows[k].id;

   // for(var i=0;i<tb.rows[k].cells.length;i++){

    //    console.log(tb.rows[k].cells[i].innerHTML);

    //}

}
return arrData;
}

Array.prototype.in_array = function(e)  
{  
for(i=0;i<this.length;i++)  
{  
if(this[i] == e)  
return true;  
}  
return false;  
} 