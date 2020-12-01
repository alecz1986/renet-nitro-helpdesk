<xsl:stylesheet version="1.0" xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <div id='site-header'>
      <a class='logo' href='/' title="Интернет-магазин Пешка, Саратов">Пешка</a>
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
  </xsl:template>
</xsl:stylesheet>
