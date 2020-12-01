<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <html>
      <head>
       <meta http-equiv="Content-Type" content="text/html;charset=koi8-r" />
       <title><xsl:value-of select="/R/page/title"/></title>
       <link rel="stylesheet" type="text/css" href="http://svetka.office.renet.int/data/basic.css" />
       <link rel="stylesheet" type="text/css" href="http://svetka.office.renet.int/highslide/highslide.css" />
       <script type="text/javascript" src="http://svetka.office.renet.int/highslide/highslide.js"></script>
       <script type="text/javascript" src="/data/html_tag.js"></script>
       <xi:bind name="page:head"/>
      </head>
      <!--      <body onLoad="javascript:print('');">-->
      <body onLoad="javascript:print('');">
      <xsl:for-each select='/R/data/prod'>
        <table border='0' width='60%' align='center'>
          <tr><td colspan='3'>
             <a href='/'> Главная </a>
             <xsl:for-each select="/R/data/categorys/category">
               <![CDATA[ / ]]>
               <xsl:element name='a'>
                 <xsl:attribute name='href'>/<xsl:value-of select="@template"/>?category_id=<xsl:value-of select="@id"/></xsl:attribute>
                 <xsl:value-of select="@name"/>
               </xsl:element>
             </xsl:for-each>
             <h1></h1>
          </td></tr>
          <tr><td colspan='2'>
              <h3><xsl:value-of select="/R/data/prod/@name"/></h3><br/>
          </td>
          <td align='right'>
            <div class='prod_info'>
             <xsl:element name='a'>
                 <xsl:attribute name='target'>_blank</xsl:attribute>
                 <xsl:attribute name='href'>/product_print?product_id=<xsl:value-of select="@id"/></xsl:attribute>
                 напечатать <br/>карточку продукта
             </xsl:element>
           </div>
         </td></tr>
         <tr><td>
                  <xsl:element name='a'>
                    <xsl:attribute name='href'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="@path"/>/<xsl:value-of select="@photo"/>.png</xsl:attribute>
                    <xsl:attribute name='onclick'>return hs.expand(this,
                          {wrapperClassName: 'borderless floating-caption', dimmingOpacity: 0.75, align: 'center'})</xsl:attribute>
                    <xsl:element name='img'>
                      <xsl:attribute name='src'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="@path"/>/<xsl:value-of select="@photo"/>_small.png</xsl:attribute>
                      <xsl:attribute name="border">0</xsl:attribute>
                    </xsl:element>
                  </xsl:element>
           </td>
           <td>
              <xsl:copy-of select="./discription"><xsl:apply-templates name="copy"/></xsl:copy-of>
           </td>
           <td class='prod'>
             <xsl:if test="@old_price!='0.00'">
               <span class="price"><s><xsl:value-of select="@old_price"/><xsl:text>.-</xsl:text></s></span>
               <br/>
               <br/>
             </xsl:if>
             <span class="price"><xsl:value-of select="@price"/>.-</span><br/>
             <xsl:if test='/R/data/categorys/category'>
              <xsl:element name='a'>
                <xsl:attribute name="href">add2cart?product_id=<xsl:value-of select='@id'/>&#38;path_info=<xsl:value-of select='/R/page/path_info'/></xsl:attribute>
                <xsl:attribute name="class">buy</xsl:attribute>
                купить
              </xsl:element>
            </xsl:if>
            <br/>
              <xsl:for-each select="/R/data/prod/mark/star">
                <xsl:element name='img'>
                  <xsl:attribute name='src'><xsl:value-of select="@uri"/></xsl:attribute>
                </xsl:element>
              </xsl:for-each>
              <br/>
             Голосов: <xsl:value-of select="/R/data/prod/mark"/><br/>
             <b>Оценить продукт: </b><br/><br/>
             <xsl:for-each select="/R/data/prod/mark/vote">
              <xsl:element name='a'>
                <xsl:attribute name='id'>mark<xsl:value-of select="@id"/></xsl:attribute>
                <xsl:attribute name='onMouseOver'>starover(<xsl:value-of select="@id"/>)</xsl:attribute>
                <xsl:attribute name='onMouseOut'>starout()</xsl:attribute>
                 <xsl:attribute name='class'>mark</xsl:attribute>
                 <xsl:attribute name='href'>/mark?mark=<xsl:value-of select="@id"/>&amp;product_id=<xsl:value-of select="/R/data/prod/@id"/></xsl:attribute>
                 <xsl:attribute name='alt'><xsl:value-of select="@vote"/></xsl:attribute>
                 <xsl:attribute name='title'><xsl:value-of select="@vote"/></xsl:attribute>
                 &#160;
               </xsl:element>
             </xsl:for-each>
             <br/>
             <xsl:element name='a'>
               <xsl:attribute name='href'>/comment?product_id=<xsl:value-of select="@id"/></xsl:attribute>
               <xsl:value-of select="/R/data/prod/comment/@count"/>
             </xsl:element> отзывов<br/>
             <xsl:element name='a'>
             <xsl:attribute name='href'>/comment?product_id=<xsl:value-of select="@id"/></xsl:attribute>
                оставить
              </xsl:element> отзыв <br/>
          </td></tr>
          <tr><td colspan='3'>
              <xsl:for-each select="/R/data/prod/photo">
                  <xsl:element name='a'>
                    <xsl:attribute name='href'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="@path"/>/<xsl:value-of select="@name"/>.png</xsl:attribute>
                    <xsl:attribute name='onclick'>return hs.expand(this,
                          {wrapperClassName: 'borderless floating-caption', dimmingOpacity: 0.75, align: 'center'})</xsl:attribute>
                    <xsl:element name='img'>
                      <xsl:attribute name='src'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="@path"/>/<xsl:value-of select="@name"/>_small.png</xsl:attribute>
                      <xsl:attribute name="border">0</xsl:attribute>
                      <xsl:attribute name="width"><xsl:value-of select='@small_x'/></xsl:attribute>
                      <xsl:attribute name="height"><xsl:value-of select='@small_y'/></xsl:attribute>
                    </xsl:element>
                  </xsl:element>
            </xsl:for-each>
          </td></tr>
          <tr><td colspan='3'>
             <ul class='tehnical'>
               <xsl:for-each select="/R/data/prod/tehnicals/tehnical">
                 <li><xsl:value-of select="@name"/>: <xsl:value-of select="@val"/></li>
               </xsl:for-each>
             </ul>
         </td></tr>
         <tr><td colspan='3'>
             <h3 css:color="#C50069">Отзывы покупателей:</h3>
         </td></tr>
         <xsl:for-each select='/R/data/comments/comment'>
          <tr><td><b><xsl:value-of select="@name"/></b>:</td><td colspan='2'><p><xsl:value-of select="@comment"/></p></td></tr>
         </xsl:for-each>
      </table>
    </xsl:for-each>
   </body>
 </html>
  </xsl:template>
  <xsl:template match="copy">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
