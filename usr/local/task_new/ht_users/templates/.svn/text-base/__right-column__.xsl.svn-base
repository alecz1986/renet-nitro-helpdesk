<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
    <xsl:template match="/">
      <!--<div class='right-column'>-->
        <a href='/auto?category_id=321319'><img border='0' src='/data/box_button.jpg'/></a>
        <br/>
        <div class='user-menu'>
          <xsl:choose>
            <xsl:when test="/R/user/authorized or /R/data/auth_ok">
              <a href="/public">Мой счет</a> | <a href="/public/auth">Выйти</a>
           </xsl:when>
           <xsl:otherwise>
              <a href="/register">Регистрация</a> | <a href="/public/auth/">Вход</a> 
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
        <a href='/start_desk?category_id=320682' width='234px' height='110px'><img border='0' src='/knopka2.gif' css:padding='10px 0px'/></a>
        <br/>
        <xi:bind name="banners-right"/>
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
      <xi:bind name="banners-right-bottom"/>
     <div class='clear'></div>
     <!--    </div>-->
  </xsl:template>
</xsl:stylesheet>
