<xsl:stylesheet version="1.0" xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <title><xsl:value-of select="/R/page/title"/></title>
    <xsl:element name='link'>
      <xsl:attribute name='rel'>stylesheet</xsl:attribute>
      <xsl:attribute name='type'>text/css</xsl:attribute>
      <xsl:attribute name='href'>/css/<xsl:value-of select='/R/page/@css'/></xsl:attribute>
    </xsl:element>
    <link rel="stylesheet" type="text/css" href="/data/highslide/highslide.css" />
    <link rel="icon" href="/favicon.ico" type="image/x-icon"/>
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon"/> 
    <script type="text/javascript" src="/data/highslide/highslide.js"></script>
    <script type="text/javascript" src="/js/jquery-1.2.6.js"></script>
    <script type="text/javascript" src="/js/swf.js"></script>
    <script type="text/javascript" src="/data/html_tag.js"></script>
    <script type="text/javascript" src="/js/jquery-1.2.6.js"></script>
    <script type="text/javascript" src="/js/height.js"></script>
    <script type="text/javascript" src="/data/star.js"></script>
    <xsl:choose>
      <xsl:when test="/R/data/kws">
        <xsl:element name="META">
          <xsl:attribute name="name">keywords</xsl:attribute>
          <xsl:attribute name="content">
            <xsl:value-of select="/R/data/kws/@kw"/>
          </xsl:attribute>
        </xsl:element>
      </xsl:when>
      <xsl:otherwise>
        <xsl:element name="META">
          <xsl:attribute name="name">keywords</xsl:attribute>
          <xsl:attribute name="content">
            <xsl:text>интернет-магазин пешка, саратов,первый в саратове интернет-магазин необходимых вещей саратов</xsl:text>
          </xsl:attribute>
        </xsl:element>
      </xsl:otherwise>
    </xsl:choose>
    <META name="description" content="интернет-магазин Пешка. Первый интернет-магазин Саратова необходимых вещей"/>
    <meta name="google-site-verification" content="kXaKKJNVSQn6wTPkZOLiWL2oLPE2s4kiljmy9B47a8E" />
    <meta name='yandex-verification' content='' />
    <!--    <script type="text/javascript">
      hs.graphicsDir = 'http://svetka.office.renet.int/highslide/graphics/';
    </script>                                                                                                                       -->
    <xi:bind name="page:head"/>
  </head>
  <body onLoad='start()'>
    <div id='site-header'>
      <a class='logo' href='/'>Пешка</a>
      <div class='pink'></div>
      <a class='slogan' href='/'>Первый в Саратове Интернет-магазин необходиых вещей</a>
      <ul class='menu'>
        <xsl:for-each select="/R/page/inf_pages/info_page">
          <li>
            <xsl:element name='a'>
              <xsl:attribute name='href'>/inf_page?inf_page=<xsl:value-of select="@link"/></xsl:attribute>
              <xsl:attribute name='css:white-space'><xsl:text>pre-wrap</xsl:text></xsl:attribute>
              <xsl:value-of select="@name"/>
            </xsl:element>
          </li>
        </xsl:for-each>
      </ul>
      <div class='order corners'>
        <div class='red'>Заказ и консультации:</div>
        <div class='red big'><span class='grey'>(8452)</span>277-877</div>
        <div class='red'><span class='grey'>email:</span> peshca@sarbc.ru</div>
        <div class='red'><span class='grey'>ICQ:</span> 617-305-097, 643-784-955</div>
        <p>Мы доставляем заказы в удобное для ВАС время, с 9 до 18 часов, по будням</p>
        <div class='corner'></div>
      </div>
    </div>
    <div id='site-center'>
      <!--       <object width='100%'>
         <embed src="http://peshca.ru/data/P_podguznik615x60.swf?clickTAG=http://peshca.ru/category?category_id=232275" width='1000' height='100'> </embed>
       </object>-->
       <!--       <div class='banner top-banner'>
	      <object width="100%">
	        <xsl:element name="embed">
	          <xsl:attribute name="src">
	            <xsl:value-of select="/R/page/banner_center"/>
	          </xsl:attribute>
	          <xsl:attribute name="width"><xsl:text>1000</xsl:text></xsl:attribute>
            <xsl:attribute name="height"><xsl:text>80</xsl:text></xsl:attribute>
            <xsl:attribute name="wmode">transparent</xsl:attribute>
	        </xsl:element>
          <param name="wmode" value="transparent"/>
	      </object>
      </div>-->
      <!--      <div width='100%' align='center' css:background-image="url('http://peshca.ru/1.jpg')">
        <noindex>
                    <script type='text/javascript'><xsl:comment><![CDATA[
                var RndNum4NoCash = Math.round(Math.random() * 1000000000);
                var ar_Tail='unknown'; if (document.referrer) ar_Tail = escape(document.referrer);
                document.write(
                '<iframe src="http://ad.adriver.ru/cgi-bin/erle.cgi?'
                  + 'sid=1&bt=36&ad=242171&pid=485062&bn=485062&rnd=' + RndNum4NoCash + '&tail256=' + ar_Tail
                  + '" frameborder=0 vspace=0 hspace=0 width=728 height=90 marginwidth=0'
                  + ' marginheight=0 scrolling=no></iframe>');
           //]]></xsl:comment></script>
           <noscript>
              <a href="http://ad.adriver.ru/cgi-bin/click.cgi?sid=1&amp;bt=36&amp;ad=242171&amp;pid=485062&amp;bn=485062&amp;rnd=1015867144" target="_blank">
                <img src="http://ad.adriver.ru/cgi-bin/rle.cgi?sid=1&amp;bt=36&amp;ad=242171&amp;pid=485062&amp;bn=485062&amp;rnd=1015867144" alt="-AdRiver-" border='0' width='728' height='90'/></a>
            </noscript>
      </noindex>
    </div>-->
      <!-- left column -->
      <div class='center-column' css:padding-right='0px'>
        <noindex>
        <xsl:if test='/R/page/@banner="3"'>

          <script type='text/javascript'><xsl:comment>//<![CDATA[
                   var ox_u = 'http://abz.peshca.ru/www/delivery/al.php?zoneid=10&layerstyle=simple&align=center&valign=top&padding=2&closetime=10&padding=2&shifth=0&shiftv=0&closebutton=t&backcolor=FFFFFF&noborder=t';
                      if (document.context) ox_u += '&context=' + escape(document.context);
                         document.write("<scr"+"ipt type='text/javascript' src='" + ox_u + "'></scr"+"ipt>");
                     //]]></xsl:comment></script>
        </xsl:if>
        <xsl:if test='/R/page/@banner="5"'>

          <script type='text/javascript'><xsl:comment>//<![CDATA[
                   var ox_u = 'http://abz.peshca.ru/www/delivery/al.php?zoneid=11&layerstyle=simple&align=center&valign=top&padding=2&padding=2&shifth=0&shiftv=0&closebutton=t&backcolor=FFFFFF&noborder=t';
                      if (document.context) ox_u += '&context=' + escape(document.context);
                         document.write("<scr"+"ipt type='text/javascript' src='" + ox_u + "'></scr"+"ipt>");
                     //]]></xsl:comment></script>
               </xsl:if>
             </noindex>
        <!--        <h4>Если Вы не нашли интересующий Вас товар, Вы можете заполнить <a href='/claim'>заявку</a>.</h4>-->
    <br/>
        <!--        <h1><xsl:value-of select='/R/page/title'/></h1>-->
        <xsl:if test="/R/data/@auto = '1'">
          <xi:bind name="form1"/>
        </xsl:if>
        <xi:bind name="body"/>
        <xi:bind name="menu"/>
        <xi:bind name="form"/>
        <xsl:if test="/R/errors/error | /R/results/result">
          <table class="menu">
            <tbody>
              <xsl:for-each select="/R/errors/error">
                <tr><td><div css:color="red"><xsl:value-of select="."/></div></td></tr>
              </xsl:for-each>
              <xsl:for-each select="/R/results/result">
                <tr><td><div css:color="blue"><xsl:value-of select="."/></div></td></tr>
              </xsl:for-each>
            </tbody>
          </table>
          <br/>
        </xsl:if>
      </div>
      <div class='left-column' css:padding-top="5px">
        <form class='search' action="/searchstring" method="get">
          <xsl:element name="input">
            <xsl:attribute name="class">input</xsl:attribute>
            <xsl:attribute name="type">text</xsl:attribute>
            <xsl:attribute name="name">s</xsl:attribute>
            <xsl:attribute name="value">
              <xsl:choose>
                <xsl:when test="/R/data/@s"> 
                  <xsl:value-of select="/R/data/@s"/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:text>поиск</xsl:text>
                </xsl:otherwise>
              </xsl:choose>
            </xsl:attribute>
          </xsl:element>
          <input class='submit' type='submit' value='OK'/>
        </form>
        <xsl:call-template name="k_object">
          <xsl:with-param name="k_iter" select="/R/page/category"/>
        </xsl:call-template>
        <div class='user-menu' css:width="192px" css:font-size="9px" css:margin="5px" css:padding="0px">
          <xsl:choose>
            <xsl:when test="/R/user/authorized or /R/data/auth_ok">
              <a href="/public" css:padding="2px">Мой счет</a> | <a css:padding="2px" href="/public/auth">Выйти</a>
           </xsl:when>
           <xsl:otherwise>
              <a href="/register" css:padding="2px">Регистрация</a> | <a href="/public/auth/" css:padding="2px">Вход в кабинет</a> 
           </xsl:otherwise>
          </xsl:choose>
        </div>
        <div class='basket corners' id='basket'>
         <noindex>
            <div css:display='none' id='last_url'><xsl:value-of select='/R/page/path_encode'/></div>
          <xsl:element name='a'>
            <xsl:attribute name='href'>/mycart?<xsl:text>&amp;path=</xsl:text><xsl:value-of select='/R/page/path_encode'/></xsl:attribute>
            <b>Ваша корзина:</b>
          </xsl:element>
          <xsl:choose>
            <xsl:when test="/R/page/@amount=0">
              <p><em>пуста</em></p>
              <br/>
            </xsl:when>
            <xsl:otherwise>
              <p><em><xsl:value-of select='/R/page/@add2cart'/></em> товар<br/>на сумму <em><xsl:value-of select='/R/page/@amount'/> р.</em></p>
            </xsl:otherwise>
          </xsl:choose>
          <div class='corner'></div>
         </noindex>
        </div>
        <br/>
        <xsl:if test="/R/data/@inf = '1'">
          <div class='news corners'>
            <h3>Полезная информация</h3>
            <xsl:for-each select='/R/page/inf_pages/info_page'>
              <xsl:if test="./@test='1'">
                <p>
                  <xsl:element name='a'>
                    <xsl:attribute name='href'>/inf_page?inf_page=<xsl:value-of select="@link"/></xsl:attribute>
                    <xsl:attribute name='css:white-space'><xsl:text>pre-wrap</xsl:text></xsl:attribute>
                    <xsl:value-of select='@name'/> 
                  </xsl:element>
                </p>
              </xsl:if>
            </xsl:for-each>
            <div class='corner'></div>
          </div>
        </xsl:if>
        <div>
          <noindex>
                        <script type='text/javascript'><xsl:comment><![CDATA[
                document.MAX_ct0 ='';

           var m3_u = (location.protocol=='https:'?'https://abz.peshca.ru/www/delivery/ajs.php':'http://abz.peshca.ru/www/delivery/ajs.php');
           var m3_r = Math.floor(Math.random()*99999999999);
           if (!document.MAX_used) document.MAX_used = ',';
           document.write ("<scr"+"ipt type='text/javascript' src='"+m3_u);
           document.write ("?zoneid=5");
           document.write ('&amp;cb=' + m3_r);
           if (document.MAX_used != ',') document.write ("&amp;exclude=" + document.MAX_used);
           document.write (document.charset ? '&amp;charset='+document.charset : (document.characterSet ? '&amp;charset='+document.characterSet : ''));
           document.write ("&amp;loc=" + escape(window.location));
           if (document.referrer) document.write ("&amp;referer=" + escape(document.referrer));
           if (document.context) document.write ("&context=" + escape(document.context));
           if ((typeof(document.MAX_ct0) != 'undefined') && (document.MAX_ct0.substring(0,4) == 'http')) {
           document.write ("&amp;ct0=" + escape(document.MAX_ct0));
           }
           if (document.mmm_fo) document.write ("&amp;mmm_fo=1");
           document.write ("'><\/scr"+"ipt>");
           //]]></xsl:comment></script><noscript>
          <a href='http://abz.peshca.ru/www/delivery/ck.php?n=a278ed0c&amp;cb=7' target='_blank'><img src='http://abz.peshca.ru/www/delivery/avw.php?zoneid=5&amp;cb=8&amp;n=a278ed0c&amp;ct0=' border='0' alt='интернет магазин Саратов' /></a>
          </noscript>
                        <script type='text/javascript'><xsl:comment><![CDATA[
                document.MAX_ct0 ='';

           var m3_u = (location.protocol=='https:'?'https://abz.peshca.ru/www/delivery/ajs.php':'http://abz.peshca.ru/www/delivery/ajs.php');
           var m3_r = Math.floor(Math.random()*99999999999);
           if (!document.MAX_used) document.MAX_used = ',';
           document.write ("<scr"+"ipt type='text/javascript' src='"+m3_u);
           document.write ("?zoneid=8");
           document.write ('&amp;cb=' + m3_r);
           if (document.MAX_used != ',') document.write ("&amp;exclude=" + document.MAX_used);
           document.write (document.charset ? '&amp;charset='+document.charset : (document.characterSet ? '&amp;charset='+document.characterSet : ''));
           document.write ("&amp;loc=" + escape(window.location));
           if (document.referrer) document.write ("&amp;referer=" + escape(document.referrer));
           if (document.context) document.write ("&context=" + escape(document.context));
           if ((typeof(document.MAX_ct0) != 'undefined') && (document.MAX_ct0.substring(0,4) == 'http')) {
           document.write ("&amp;ct0=" + escape(document.MAX_ct0));
           }
           if (document.mmm_fo) document.write ("&amp;mmm_fo=1");
           document.write ("'><\/scr"+"ipt>");
           //]]></xsl:comment></script><noscript>
          <a href='http://abz.peshca.ru/www/delivery/ck.php?n=a5af0cb1&amp;cb=7' target='_blank'><img src='http://abz.peshca.ru/www/delivery/avw.php?zoneid=8&amp;cb=8&amp;n=a5af0cb1&amp;ct0=' border='0' alt='интернет магазин Саратов' /></a>
          </noscript>
          <br/>
                        <script type='text/javascript'><xsl:comment><![CDATA[
                document.MAX_ct0 ='';

           var m3_u = (location.protocol=='https:'?'https://abz.peshca.ru/www/delivery/ajs.php':'http://abz.peshca.ru/www/delivery/ajs.php');
           var m3_r = Math.floor(Math.random()*99999999999);
           if (!document.MAX_used) document.MAX_used = ',';
           document.write ("<scr"+"ipt type='text/javascript' src='"+m3_u);
           document.write ("?zoneid=9");
           document.write ('&amp;cb=' + m3_r);
           if (document.MAX_used != ',') document.write ("&amp;exclude=" + document.MAX_used);
           document.write (document.charset ? '&amp;charset='+document.charset : (document.characterSet ? '&amp;charset='+document.characterSet : ''));
           document.write ("&amp;loc=" + escape(window.location));
           if (document.referrer) document.write ("&amp;referer=" + escape(document.referrer));
           if (document.context) document.write ("&context=" + escape(document.context));
           if ((typeof(document.MAX_ct0) != 'undefined') && (document.MAX_ct0.substring(0,4) == 'http')) {
           document.write ("&amp;ct0=" + escape(document.MAX_ct0));
           }
           if (document.mmm_fo) document.write ("&amp;mmm_fo=1");
           document.write ("'><\/scr"+"ipt>");
           //]]></xsl:comment></script><noscript>
          <a href='http://abz.peshca.ru/www/delivery/ck.php?n=aa5de9d2&amp;cb=7' target='_blank'><img src='http://abz.peshca.ru/www/delivery/avw.php?zoneid=9&amp;cb=8&amp;n=aa5de9d2&amp;ct0=' border='0' alt='интернет магазин Саратов' /></a>
          </noscript>
          <!--          <object width="170" height="300">
            <param name="wmode" value="transparent"/>
            <embed src="http://peshca.ru/data/technic.swf?clickTAG=http://peshca.ru/category?category_id=321136" width="170" height="300" wmode="transparent"/>
          </object>-->
        </noindex>
        </div>
      </div>
      <!-- end if left column -->
      <!-- center column -->
      <!-- width:75%-->
    </div>
    <div id='site-footer'>
    <script>
    	$("#site-footer").css("top" , $(document).height()+'px');
    	$("#creepingline").css("width" , $(document).width()-500+'px');
    	$("#site-footer").css("width" , "95%");
    </script>
      <a class='logo' href='' title="Интернет-магазин Пешка, Саратов">Пешка</a>
      <ul class='menu'>
         <li><a href="/pricelist">Прайс-лист</a></li>
         <li><a href="/feedback">Обратная связь</a></li>
         <li><a href="/news">Новости</a></li>
         <li><a href="/order_status">Статус заказа</a></li>
         <li><a href="/sale">Акции</a></li>
         <li><a href="/senderror">Пожаловаться на работу магазина</a></li>
      </ul>
      <p>Обращаем ваше внимание на то, что данный интернет-сайт носит исключительно информационный характер и ни при каких условиях не является публичной офертой, определяемой положениями Статьи 437 (2) Гражданского кодекса Российской Федерации. Для получения подробной информации о наличии и стоимости указанных товаров и (или) услуг, пожалуйста, обращайтесь к менеджерам отдела клиентского обслуживания с помощью специальной формы связи или по телефону: (8452) 277-877.</p>
      <div class='counters'>
        <div id='mailcount'>
          <script language="javascript" type="text/javascript">
            <xsl:comment><![CDATA[
              d=document;var a='';a+=';r='+escape(d.referrer);js=10;//]]></xsl:comment>
          </script>
          <script language="javascript1.1" type="text/javascript"><xsl:comment><![CDATA[
              a+=';j='+navigator.javaEnabled();js=11;//]]></xsl:comment></script>
          <script language="javascript1.2" type="text/javascript"><xsl:comment><![CDATA[
              s=screen;a+=';s='+s.width+'*'+s.height;a+=';d='+(s.colorDepth?s.colorDepth:s.pixelDepth);js=12;//]]></xsl:comment></script>
          <script language="javascript1.3" type="text/javascript"><xsl:comment><![CDATA[
              js=13;//]]></xsl:comment></script>
          <script language="javascript" type="text/javascript"><xsl:comment><![CDATA[
              d.write('<a href="http://top.mail.ru/jump?from=1620680" target="_top">'+'<img src="http://da.cb.b8.a1.top.mail.ru/counter?id=1620680;t=213;js='+js+a+';rand='+Math.random()+'" alt="Рейтинг@Mail.ru" border="0" '+'height="31" width="88"><\/a>');//]]></xsl:comment></script>
          <noscript><a target="_top" href="http://top.mail.ru/jump?from=1620680"><img src="http://da.cb.b8.a1.top.mail.ru/counter?js=na;id=1620680;t=213" height="31" width="88" border="0" alt="Рейтинг@Mail.ru"/></a></noscript>
        </div>
        <div class='counter'><img alt="http://sarbc.ru" title="" src='http://de-fis.ru/peshka/img/counters/sarbc.gif'/></div>
        <div class='counter'>
          <script type="text/javascript"><xsl:comment><![CDATA[
                document.write("<a href='http://www.liveinternet.ru/click' "+
                  "target=_blank><img src='//counter.yadro.ru/hit?t44.4;r"+
                    escape(document.referrer)+((typeof(screen)=="undefined")?"":
                    ";s"+screen.width+"*"+screen.height+"*"+(screen.colorDepth?
                    screen.colorDepth:screen.pixelDepth))+";u"+escape(document.URL)+
                    ";"+Math.random()+
                    "' alt='' title='LiveInternet' "+
                    "border='0' width='31' height='31'><\/a>")
              ]]></xsl:comment>
          </script>
        </div>
        <div class='counter'>
          <script src="//mc.yandex.ru/metrika/watch.js" type="text/javascript"></script>
          <div css:display="none"><script type="text/javascript">
              try { var yaCounter1598497 = new Ya.Metrika(1598497);
              yaCounter1598497.clickmap();
              yaCounter1598497.trackLinks({external: true});
              } catch(e){}
          </script></div>
          <noscript><div css:position="absolute"><img src="http://mc.yandex.ru/watch/1598497" alt="" /></div></noscript>
        </div>
        <div class="counter">
          <script id="top100Counter" type="text/javascript" src="http://counter.rambler.ru/top100.jcn?2166435"></script>
          <noscript>
            <img src="http://counter.rambler.ru/top100.cnt?2166435" alt="" width="1" height="1" border="0" />
          </noscript>
          <script id="top100Counter" type="text/javascript" src="http://counter.rambler.ru/top100.jcn?2166435"></script>
          <noscript>
            <img src="http://counter.rambler.ru/top100.cnt?2166435" alt="" width="1" height="1" border="0" />
          </noscript>
        </div>
      </div>
      <div class='clear'></div>
    </div>
    <script type="text/javascript">
      var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
      document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
      try {
      var pageTracker = _gat._getTracker("UA-304907-12");
      pageTracker._trackPageview();
      } catch(err) {}</script>
  </body>
</html>
  </xsl:template>
  <xsl:template name="k_object">
    <xsl:param name="k_iter" select="."/>
    <xsl:param name="name" select="./@name"/>
    <xsl:if test="($k_iter)/*">
      <ul class="menu">
        <xsl:for-each select="($k_iter)/*">
          <xsl:if test="@opt=/R/data/@opt">
            <li>
              <xsl:element name='a'>
                 <xsl:attribute name="css:white-space"><xsl:text>pre-wrap</xsl:text></xsl:attribute>
                 <xsl:attribute name='href'>/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select='@id'/></xsl:attribute>
                <xsl:if test="@action = 'true'">
                  <xsl:attribute name='class'>click</xsl:attribute>
                </xsl:if>
                <xsl:if test="@new = 'ye'">
                  <xsl:attribute name='css:text-decoration'>underline</xsl:attribute>
                  <xsl:attribute name='css:color'>#C50069</xsl:attribute>
                </xsl:if>
                <xsl:choose>
                  <xsl:when test="@action = 'true' and @root!='0'">
                    <xsl:text> - </xsl:text>
                 </xsl:when>
                 <xsl:otherwise>
                    <xsl:if test="@plus='1' and @root!='0'">
                      <xsl:text> + </xsl:text>
                    </xsl:if>
                    <xsl:if test="@plus='0' and @root!='0'">
                      <xsl:text> - </xsl:text>
                    </xsl:if>
                 </xsl:otherwise>
                </xsl:choose>
               <xsl:value-of select="@name"/>
               <!--                <script>
                  br("<xsl:value-of select='@name'/>")
                </script>-->
              </xsl:element>
              <xsl:call-template name="k_object"/>
            </li>
          </xsl:if>
        </xsl:for-each>
      </ul>
    </xsl:if>
  </xsl:template>
  <xsl:template match="copy">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
