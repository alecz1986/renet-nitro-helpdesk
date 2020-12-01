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
    <!--    <link rel="stylesheet" type="text/css" href="/css/basic.css" />-->
    <link rel="stylesheet" type="text/css" href="/data/highslide/highslide.css" />
    <script type="text/javascript" src="/data/highslide/highslide.js"></script>
    <script type="text/javascript" src="/js/swf.js"></script>
    <script type="text/javascript" src="/js/jquery-1.2.6.js"></script>
    <script type="text/javascript" src="/js/height.js"></script>
    <script type="text/javascript" src="/data/html_tag.js"></script>
    <script type="text/javascript" src="/data/star.js"></script>
    <xsl:choose>
      <xsl:when test="/R/data/kws">
        <xsl:element name="META">
          <xsl:attribute name="name">content</xsl:attribute>
          <xsl:attribute name="content">
            <xsl:value-of select="/R/data/kws/@kw"/>
          </xsl:attribute>
        </xsl:element>
      </xsl:when>
      <xsl:otherwise>
        <xsl:element name="META">
          <xsl:attribute name="name">content</xsl:attribute>
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
    <script type="text/javascript">
      function add2cart(id){
      res = document.getElementById('res');
      res.value=res.value+'p'+id+'_'+document.getElementById(id).value;
      }
    </script>
    <script type="text/javascript">
        function test()
        {
            /*
            alert(document.getElementsByTagName('body')[0].style.backgroundColor);
            document.getElementsByTagName('body')[0].style.backgroundColor='#ffffff';
            */
            var z1=document.getElementById('z1');
            z1.style.display='none';
            var header=document.getElementById('site-header');
            header.style.display='block';

            var center=document.getElementById('site-center');
            center.style.display='block';

            var footer=document.getElementById('site-footer');
            footer.style.display='block';
        }
        setTimeout('test()',6000);
    </script>
    <xsl:if test='/R/page/picture/@check'>
      <style type="text/css">
          /* body{background-color:#0064FD !important} */
          #z1{display:block;}
          #site-header{display:none;}
          #site-center{display:none;}
          #site-footer{display:none;}
      </style>
      <div  id='z1' align='center'>
        <object codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0" id="z1" align="middle" width='100%' height='600px'>
          <param name="allowScriptAccess" value="sameDomain" />
          <param name="movie" value="z1.swf" />
          <param name="quality" value="high" />
          <param name="bgcolor" value="#ffffff" />
          <embed src="/data/z1.swf" quality="high" bgcolor="#ffffff" width='100%' height='600px' name="z1" align="middle" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" />
        </object>
      </div>
    </xsl:if>
    <div id='site-header'>
      <a class='logo' href='/' title="Интернет-магазин Пешка, Саратов">Пешка</a>
      <div class='pink'></div>
      <a class='slogan' href='/'>Первый в Саратове Интернет-магазин необходиых вещей</a>
      <ul class='menu'>
        <xsl:for-each select="/R/page/inf_pages/info_page">
          <li>
            <xsl:element name='a'>
              <xsl:attribute name='href'>/inf_page?inf_page=<xsl:value-of select="@link"/></xsl:attribute>
              <xsl:value-of select="@name"/>
            </xsl:element>
          </li>
        </xsl:for-each>
      </ul>
      <div class='order corners'>
        <div class='red'>Заказ и консультации:</div>
        <div class='red big'><span class='grey'>(8452)</span>277-877</div>
        <div class='red'><span class='grey'>email:</span> peshca@sarbc.ru</div>
        <div class='red'><span class='grey'>ICQ:</span> 552-070-862</div>
        <p>Мы доставляем заказы в удобное для ВАС время, с 9 до 18 часов, по будням</p>
        <div class='corner'></div>
      </div>
    </div>
    <div id='site-center'>
      <div width='100%' align='center' css:background-image="url('http://peshca.ru/1.jpg')">
                                <script type='text/javascript'><xsl:comment><![CDATA[
                document.MAX_ct0 ='';

           var m3_u = (location.protocol=='https:'?'https://abz.peshca.ru/www/delivery/ajs.php':'http://abz.peshca.ru/www/delivery/ajs.php');
           var m3_r = Math.floor(Math.random()*99999999999);
           if (!document.MAX_used) document.MAX_used = ',';
           document.write ("<scr"+"ipt type='text/javascript' src='"+m3_u);
           document.write ("?zoneid=4");
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
        <a href='http://abz.peshca.ru/www/delivery/ck.php?n=a84f4e7f&amp;cb=5' target='_blank'><img src='http://abz.peshca.ru/www/delivery/avw.php?zoneid=4&amp;cb=6&amp;n=a84f4e7f&amp;ct0=' border='0' alt='интернет магазин Саратов' /></a>
        <br/>
      </noscript>
      <div id='creepingline'>
        <iframe frameborder='0' scrolling='no' marginheight='0' marginwidth='0' style='height:20px;' src='/test2.html'></iframe>
      </div>
    <!-- AdRiver code START: Управление ротацией: код сценария; AD: 236779 "MEGAFON_REGION_TEST";   сценарий   ID 468239 "code" ; 240x400 -->
    <!--    <script language="javascript" type="text/javascript"><xsl:comment><![CDATA[
      var RndNum4NoCash = Math.round(Math.random() * 1000000000);
      var ar_Tail='unknown'; if (document.referrer) ar_Tail = escape(document.referrer);
      document.write(
      '<iframe src="http://ad.adriver.ru/cgi-bin/erle.cgi?'
        + 'sid=1&bt=22&ad=236779&pid=468239&bn=468239&rnd=' + RndNum4NoCash + '&tail256=' + ar_Tail
        + '" frameborder=0 vspace=0 hspace=0 width=1000 height=90 marginwidth=0'
        + ' marginheight=0 scrolling=no></iframe>');
      //]]></xsl:comment></script>
    <noscript>
      <a href="http://peshca.ru/category?category_id=321021" target="_blank">
        <img src="http://peshca.ru/data/megafon.swf" alt="мегафон" border='0' width='1000px' height='90px'/></a>
    </noscript>-->
      <!-- AdRiver code END -->
    </div>

      <!-- left column -->
      <div class='center-column'>
        <!--        <script src="http://www.gmodules.com/ig/ifr?url=http://www.google.com/cse/api/018071016779616941727/cse/3n3dwrodspy/gadget&amp;synd=open&amp;w=400&amp;h=90&amp;title=%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82-%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD+%D0%9F%D0%B5%D1%88%D0%BA%D0%B0&amp;border=%23ffffff%7C3px%2C1px+solid+%23999999&amp;output=js"></script>-->
        <!--        <h1><xsl:value-of select='/R/page/title'/></h1>-->
        <!--        <h4>Если Вы не нашли интересующий Вас товар, Вы можете заполнить <a href='/claim'>заявку</a>.</h4>-->
        <xsl:if test="/R/data/@auto = '1'">
          <xi:bind name="form1"/>
        </xsl:if>
        <xi:bind name="body"/>
        <xi:bind name="body1"/>
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
        <br/>
        <div>
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
        </div>

        <!--        <xsl:for-each select="/R/page/banners_left/banner">
          <div class='banner' border='0'>
            <xsl:element name='a'>
              <xsl:attribute name="href"><xsl:value-of select='@link'/></xsl:attribute>
              <xsl:element name='img'>
                <xsl:attribute name="alt"><xsl:value-of select='@alt'/></xsl:attribute>
                <xsl:attribute name="title"><xsl:value-of select='@title'/></xsl:attribute>
                <xsl:attribute name="src"><xsl:value-of select='/R/page/serv/@name'/>data/<xsl:value-of select='@name'/></xsl:attribute>
                <xsl:attribute name="width">192</xsl:attribute>
                <xsl:attribute name="border">0</xsl:attribute>
              </xsl:element>
            </xsl:element>
          </div>  
        </xsl:for-each>-->
      </div>
      <!-- end if left column -->
      <!-- center column -->
      <div class='right-column'>
        <a href='/auto?category_id=321319'><img border='0' src='/data/box_button.jpg'/></a>
        <br/>
        <div class='user-menu'>
          <xsl:choose>
            <xsl:when test="/R/user/authorized or /R/data/auth_ok">
              <a href="/public">Мой счет</a> | <a href="/public/auth">Выйти</a>
           </xsl:when>
           <xsl:otherwise>
              <a href="/register">Регистрация</a> | <a href="/public/auth/">Вход в кабинет</a> 
           </xsl:otherwise>
          </xsl:choose>
        </div>
        <div class='basket corners'>
         <noindex>
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
        <a href='/category?category_id=320682' width='234px' height='110px'><img border='0' src='/data/knopka2.png' css:padding='10px 0px'/></a>
        <br/>
                                <script type='text/javascript'><xsl:comment><![CDATA[
                document.MAX_ct0 ='';

           var m3_u = (location.protocol=='https:'?'https://abz.peshca.ru/www/delivery/ajs.php':'http://abz.peshca.ru/www/delivery/ajs.php');
           var m3_r = Math.floor(Math.random()*99999999999);
           if (!document.MAX_used) document.MAX_used = ',';
           document.write ("<scr"+"ipt type='text/javascript' src='"+m3_u);
           document.write ("?zoneid=7");
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
          <a href='http://abz.peshca.ru/www/delivery/ck.php?n=aa072b13&amp;cb=7' target='_blank'><img src='http://abz.peshca.ru/www/delivery/avw.php?zoneid=7&amp;cb=8&amp;n=aa072b13&amp;ct0=' border='0' alt='интернет магазин Саратов' /></a>
        </noscript>
          <!--        <xsl:element name="a">
          <xsl:attribute name="href">/order_desk?category_id=<xsl:value-of select="/R/page/banner_right_up/@cat_id"/></xsl:attribute>
          <xsl:attribute name="width">236px</xsl:attribute>
          <xsl:attribute name="height">110px</xsl:attribute>
          <xsl:element name="img">
            <xsl:attribute name="border">0</xsl:attribute>
            <xsl:attribute name="css:padding">10px 0px</xsl:attribute>
            <xsl:attribute name="src"><xsl:value-of select="/R/page/banner_right_up/@img"/></xsl:attribute>
          </xsl:element>
        </xsl:element>-->
        <div class='news corners'>
          <h3>Новости магазина</h3>
          <xsl:for-each select='/R/page/news/new'>
            <p>
              <em><xsl:value-of select='@date'/></em>
              <xsl:element name='a'>
                <xsl:attribute name='href'>/news?new_id=<xsl:value-of select='@uid'/></xsl:attribute>
                <xsl:value-of select='@name'/> 
              </xsl:element>
            </p>
          </xsl:for-each>
          <a class='rss' href='/rss'>RSS-подписка на новости магазина</a>
          <div class='corner'></div>
        </div>
        <div class='popular-goods goods corners'>
          <h3>Популярные товары</h3>
          <xsl:for-each select="/R/page/popular/product">
            <p>
              <xsl:element name='a'>
                <xsl:attribute name="class">thumb</xsl:attribute>
                <xsl:attribute name='href'>/product?product_id=<xsl:value-of select='@id'/></xsl:attribute>
                <xsl:element name='img'>
                  <xsl:attribute name="alt"><xsl:value-of select='@name'/></xsl:attribute>
                  <xsl:attribute name="title"><xsl:value-of select='@name'/></xsl:attribute>
                  <xsl:attribute name="src"><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select='@path'/>/<xsl:value-of select='@photo'/>_small.png</xsl:attribute>
                  <xsl:choose>
                    <xsl:when test="@small_x!='None'">
                      <xsl:attribute name="width"><xsl:value-of select='@small_x'/></xsl:attribute>
                      <xsl:attribute name="height"><xsl:value-of select='@small_y'/></xsl:attribute>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:attribute name="width">30</xsl:attribute>
                      <xsl:attribute name="height">30</xsl:attribute>
                    </xsl:otherwise>
                  </xsl:choose>
                </xsl:element>
              </xsl:element>
              <xsl:if test="@holiday = 'yes'">
                <img src='/ng_small.png' border='0' class='ng'/>
              </xsl:if>
              <span class='price'><xsl:value-of select='@price'/></span>
              <xsl:element name='a'>
                <xsl:attribute name="href">
                  <xsl:text>/add2cart?product_id=</xsl:text>
                  <xsl:value-of select='@id'/>
                  <xsl:text>&amp;path_info=</xsl:text>
                  <xsl:value-of select='/R/page/path_encode'/>
                </xsl:attribute>
                <xsl:attribute name="class">buy</xsl:attribute>
                <xsl:text>купить</xsl:text>
              </xsl:element>
              <b>
                <xsl:element name='a'>
                  <xsl:attribute name="href">
                    <xsl:text>/product?product_id=</xsl:text>
                    <xsl:value-of select='@id'/>
                  </xsl:attribute>
                  <xsl:value-of select='@name'/>
                </xsl:element>
              </b>
              <em>
                <xsl:value-of select='@overview'/>
              </em>
            </p>  
          </xsl:for-each>
        <div class='corner'></div>
      </div>
      <xsl:for-each select="/R/page/banners_right/banner">
        <div class='banner' border='0'>
          <xsl:element name='a'>
            <xsl:attribute name="href"><xsl:value-of select='@link'/></xsl:attribute>
            <xsl:element name='img'>
              <xsl:attribute name="alt"><xsl:value-of select='@alt'/></xsl:attribute>
              <xsl:attribute name="title"><xsl:value-of select='@title'/></xsl:attribute>
              <xsl:attribute name="src">
                <xsl:value-of select='/R/page/serv/@name'/>
                <xsl:text>data/</xsl:text>
                <xsl:value-of select='@name'/>
              </xsl:attribute>
              <xsl:attribute name="width">234</xsl:attribute>
              <xsl:attribute name="border">0</xsl:attribute>
            </xsl:element>
          </xsl:element>
        </div>  
      </xsl:for-each>
      <!--
      <object width="100%" border='0'>
        <xsl:element name="embed">
          <xsl:attribute name="src">
            <xsl:value-of select="/R/page/banner_right"/>
          </xsl:attribute>
          <xsl:attribute name="width"><xsl:text>234</xsl:text></xsl:attribute>
          <xsl:attribute name="height"><xsl:text>200</xsl:text></xsl:attribute>
          <xsl:attribute name="wmode">transparent</xsl:attribute>
          <xsl:attribute name="border">0</xsl:attribute>
        </xsl:element>
        <param name="wmode" value="transparent"/>
      </object>
      -->
      <!--/* OpenX Javascript Tag v2.8.5 */-->

      <script type='text/javascript'><xsl:comment><![CDATA[
           document.MAX_ct0 ='INSERT_CLICKURL_HERE';

           var m3_u = (location.protocol=='https:'?'https://abz.peshca.ru/www/delivery/ajs.php':'http://abz.peshca.ru/www/delivery/ajs.php');
           var m3_r = Math.floor(Math.random()*99999999999);
           if (!document.MAX_used) document.MAX_used = ',';
           document.write ("<scr"+"ipt type='text/javascript' src='"+m3_u);
           document.write ("?zoneid=6");
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
           //]]></xsl:comment></script><noscript><a href='http://abz.peshca.ru/www/delivery/ck.php?n=a7d9bd8a&amp;cb=INSERT_RANDOM_NUMBER_HERE' target='_blank'><img src='http://abz.peshca.ru/www/delivery/avw.php?zoneid=6&amp;cb=INSERT_RANDOM_NUMBER_HERE&amp;n=a7d9bd8a&amp;ct0=INSERT_CLICKURL_HERE' border='0' alt='' /></a></noscript>
      <!--      <object width='100%'>
        <embed src="http://peshca.ru/data/diski_avto_peshka.swf?clickTAG=http://peshca.ru/category?category_id=30866" width='190' height='100'> </embed>
      </object>-->
      <div class='clear'></div>
      <!-- end of right column -->
    </div>
  </div>
  <div id='site-footer'>
    <div width='10%'>
      <a class='logo' href='/' title="интернет-магазин саратов">Пешка. Интернет-магазин</a>
    </div>
    <div width='75%'>
      <ul class='menu'>
         <li><a href="/pricelist">Прайс-лист</a></li>
         <li><a href="/feedback">Обратная связь</a></li>
         <li><a href="/news">Новости</a></li>
         <li><a href="/order_status">Статус заказа</a></li>
         <li><a href="/sale">Акции</a></li>
         <li><a href="/senderror">Пожаловаться на работу магазина</a></li>
      </ul>
      <p>Обращаем ваше внимание на то, что данный интернет-сайт носит исключительно информационный характер и ни при каких условиях не является публичной офертой, определяемой положениями Статьи 437 (2) Гражданского кодекса Российской Федерации. Для получения подробной информации о наличии и стоимости указанных товаров и (или) услуг, пожалуйста, обращайтесь к менеджерам отдела клиентского обслуживания с помощью специальной формы связи или по телефону: (8452) 277-877.</p>
      </div>
      <div class='counters'>
        <div id='mailcount' class='counter'>
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
            "target=_blank><img src='//counter.yadro.ru/hit?t11.1;r"+
              escape(document.referrer)+((typeof(screen)=="undefined")?"":
              ";s"+screen.width+"*"+screen.height+"*"+(screen.colorDepth?
              screen.colorDepth:screen.pixelDepth))+";u"+escape(document.URL)+
              ";"+Math.random()+
              "' alt='' title='LiveInternet: показано число просмотров за 24"+
              " часа, посетителей за 24 часа и за сегодня' "+
              "border='0' width='88' height='31'><\/a>")
              ]]></xsl:comment>
          </script>
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
      } catch(err) {}
    </script>
  </body>
</html>
  </xsl:template>
  <xsl:template name="k_object">
    <xsl:param name="k_iter" select="."/>
    <xsl:param name="name" select="./@name"/>
    <xsl:if test="($k_iter)/*">
      <ul class="menu">
        <xsl:for-each select="($k_iter)/*">
            <li>
              <xsl:element name='a'>
                <xsl:attribute name='href'>
                  <xsl:text>/category?category_id=</xsl:text>
                  <xsl:value-of select='@id'/>
                </xsl:attribute>
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
                <script>
                  br("<xsl:value-of select='@name'/>")
                </script>
                <!--<xsl:value-of select='@name'/>-->
              </xsl:element>
              <xsl:call-template name="k_object"/>
            </li>
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
