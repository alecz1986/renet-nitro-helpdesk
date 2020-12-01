	      function onLo() {
		      var eventSource2 = new Timeplot.DefaultEventSource();

			      //обработка отмеченных данных
				var eventSource = new Timeplot.DefaultEventSource();
				var TimeGeometry = new Timeplot.DefaultTimeGeometry({});
				var eventSource2 = new Timeplot.DefaultEventSource();
				var plotInf = []

			        test_time=Timeplot.createPlotInfo({
				   id: "plot0",
				   timeGeometry: TimeGeometry,
				    eventSource: eventSource2,
				    lineColor: "#CC8080"
			       })
			        plotInf[0]=test_time
				var a = checks.split('-')
				for (var j = 0; j < a.length-1; j++){
				plotInf[j+1] =   Timeplot.createPlotInfo({
				   id: 'plot'+a[j],
				   roundValues: false,
				   dataSource: new Timeplot.ColumnSource(eventSource,a[j]),
 				   lineColor: color[a[j]-1],
				   valuesColor: color[a[j]-1],
			           showValues: true,
				   valueGeometry: new Timeplot.DefaultValueGeometry({
                                   }),
                                   timeGeometry:TimeGeometry, 
				   })
				};
			           timeplot = Timeplot.create(document.getElementById("my-timeplot"), plotInf);
//				   timeplot.loadXML("/test.xml?"+params,  eventSource2);
				   timeplot.loadXML("/private/report/event?"+params,  eventSource2);
			           timeplot.loadText("/private/report/data?"+params, ",", eventSource); 
				  var divmy = document.getElementById("my-timeplot").childNodes[0]
                                  var first = divmy.childNodes[0].id
                                  var t_id = first.split('-')[0]
                                  for (var k = 0; k < a.length-1; k++){
				  document.getElementById(t_id+'-'+'plot'+a[k]+'valueflag').style.color=color[a[k]-1]
				  document.getElementById(t_id+'-'+'plot'+a[k]+'valueflagLineLeft').style.visibility='hidden'
				  document.getElementById(t_id+'-'+'plot'+a[k]+'valueflagLineRight').style.visibility='hidden'
				  document.getElementById(t_id+'-'+'plot'+a[k]+'valueflag').style.visibility='hidden'
				  }
//				  document.getElementById('pm').value = '$ret'
//				  var interaval = document.getElementById('interval')
//				  interval.appendChild(document.createTextNode('$per'))
//				  document.getElementById('list').value='$list'
				  

				}
		 function removeChildrenRecursively(node)  
		 {  
		     if (!node) return;  
		     while (node.hasChildNodes()) {  
		         removeChildrenRecursively(node.firstChild);  
		         node.removeChild(node.firstChild);  
		     }  
		 } 
			function show_values(){
				var names = _names.split('-')
				var a = checks.split('-')
				var divmy = document.getElementById("my-timeplot").childNodes[0]
                	        var first = divmy.childNodes[0].id
                        	var t_id = first.split('-')[0]
				var div = document.getElementById('val')
				removeChildrenRecursively(div)
				var b = document.createElement('b')
				var f = document.createElement('font')
				f.setAttribute('style', 'font-size:10pt; color: #14849d')
				f.appendChild(document.createTextNode(document.getElementById(t_id+'-'+'timeflag').childNodes[0].data))
				b.appendChild(f)
				div.appendChild(b)
				div.appendChild(document.createElement('br'))
				for (var k = 0; k < a.length-1; k++){
				var t = document.getElementById(t_id+'-'+'plot'+a[k]+'valueflag').childNodes[0].data
				var font = document.createElement('font')
				font.setAttribute('style', 'font-size:8pt;')
				font.setAttribute('color', color[a[k]-1])
				font.appendChild(document.createTextNode(names[k]+': '+t))
				div.appendChild(font)
				div.appendChild(document.createElement('br'))
				}
				div.style.visibility = 'visible'}
