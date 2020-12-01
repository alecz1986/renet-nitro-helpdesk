<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <div width='10%'>
      <a class='logo' href='/' title="интернет-магазин саратов">Пешка. Интернет-магазин</a>
    </div>
    <div width='60%'>
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
  </xsl:template>
</xsl:stylesheet>
