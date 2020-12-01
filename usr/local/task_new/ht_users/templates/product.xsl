<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
    <xsl:template match="/">
      <xsl:for-each select='/R/data/prod'>
        <table border='0' id='table' css:display="none">
          <tr><td colspan='3'>
            <a href='/' css:color="#C50069" css:font-weight="bold" css:font-size="15px" css:BORDER-BOTTOM="1px dashed #C50069">Интернет-магазин "Пешка"</a>
            <xsl:for-each select="/R/data/categorys/category">
              <xsl:text> > </xsl:text>
              <xsl:element name='a'>
                <xsl:attribute name='href'>/<xsl:value-of select="@template"/>?category_id=<xsl:value-of select="@id"/></xsl:attribute>
                <xsl:attribute name='css:font-size'>15px</xsl:attribute>
                <xsl:attribute name='css:BORDER-BOTTOM'>1px dashed #C50069</xsl:attribute>
                <xsl:value-of select="@name"/>
              </xsl:element>
            </xsl:for-each>
            <br/>
            <br/>
          </td></tr>
          <tr><td colspan='2'>
              <h3><xsl:value-of select="/R/data/prod/@name"/></h3><br/>
          </td>
          <td align='right'>
            <div class='pro_info'>
             <xsl:element name='a'>
                 <xsl:attribute name='target'>_blank</xsl:attribute>
                 <xsl:attribute name='href'>/product_print?product_id=<xsl:value-of select="@id"/></xsl:attribute>
                 <font color="#C50069">напечатать <br/>карточку продукта</font>
             </xsl:element>
           </div>
         </td></tr>
         <tr><td width="200px">
                  <xsl:element name='a'>
                    <xsl:attribute name='href'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="@path"/>/<xsl:value-of select="@photo"/>.png</xsl:attribute>
                    <xsl:attribute name='onclick'>return hs.expand(this,
                          {wrapperClassName: 'borderless floating-caption', dimmingOpacity: 0.75, align: 'center'})</xsl:attribute>
                    <xsl:element name='img'>
                      <xsl:attribute name='src'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="@path"/>/<xsl:value-of select="@photo"/>_med.png</xsl:attribute>
                      <xsl:attribute name="border">0</xsl:attribute>
                    </xsl:element>
                  </xsl:element>
                  <xsl:if test="/R/data/prod/@holiday = 'yes'">
                    <xsl:element name='a'>
                      <xsl:attribute name='href'>http://peshca.ru/news?new_id=water</xsl:attribute>
                      <xsl:element name='img'>
                        <xsl:attribute name='src'>/ng.png</xsl:attribute>
                        <xsl:attribute name="border">0</xsl:attribute>
                        <xsl:attribute name="css:margin-left"><xsl:value-of select="@med_x"/>px</xsl:attribute>
                        <xsl:attribute name="class">ng_start</xsl:attribute>
                      </xsl:element>
                    </xsl:element>
                  </xsl:if>
           </td>
           <td id="prod_center">
             <xsl:copy-of select="./discription"><xsl:apply-templates name="copy"/></xsl:copy-of>
             <!--             <xsl:if test="/R/data/prod/technicals/technical">
               <ul class='technical'>
                 <xsl:for-each select="/R/data/prod/technicals/technical">
                   <li><xsl:value-of select="@name"/>: <font color="#C50069"><xsl:value-of select="@val"/></font></li>
                 </xsl:for-each>
               </ul>
             </xsl:if> -->
           </td>
           <td class='prod' width="150px">
             <xsl:if test="@old_price!=''">
               <span class="price"><s><xsl:value-of select="@old_price"/><xsl:text></xsl:text></s></span>
               <br/>
               <br/>
             </xsl:if>
             <span class="price"><xsl:value-of select="@price"/></span><br/>
             <br/>
             <xsl:if test='/R/data/categorys/category'>
               <xsl:element name='a'>
                <xsl:attribute name="href">add2cart?product_id=<xsl:value-of select='@id'/>&#38;path_info=<xsl:value-of select='/R/page/path_encode'/>&#38;opt=<xsl:value-of select='@opt'/></xsl:attribute>
                <!--                <xsl:attribute name="class">buy</xsl:attribute>
                купить-->
                <img src='/data/button_sale.png' border='0'/>
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
               задать вопрос 
              </xsl:element><br/>
          </td></tr>
          <tr><td colspan='3'>
              <xsl:for-each select="/R/data/prod/photos/photo">
                <xsl:element name='a'>
                  <xsl:attribute name="css:padding">10px</xsl:attribute>
                  <xsl:attribute name='href'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="@path"/>/<xsl:value-of select="@name"/>.png</xsl:attribute>
                  <xsl:attribute name='onclick'>
                      return hs.expand (this, { wrapperClassName: 'wide-border'})
                      <!--  return hs.expand(this,
                      {wrapperClassName: 'borderless floating-caption', dimmingOpacity: 0.75, align: 'center'})-->
                  </xsl:attribute>
                  <xsl:element name='img'>
                    <xsl:attribute name='src'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="@path"/>/<xsl:value-of select="@name"/>_small.png</xsl:attribute>
                    <xsl:attribute name="border">0</xsl:attribute>
                    <xsl:attribute name="width"><xsl:value-of select='@small_x'/></xsl:attribute>
                    <xsl:attribute name="height"><xsl:value-of select='@small_y'/></xsl:attribute>
                  </xsl:element>
                </xsl:element>
            </xsl:for-each>
          </td></tr>
          <tr><td colspan='3' class='disc'>
                          <xsl:if test="/R/data/prod/technicals/technical">
               <ul class='technical'>
                 <xsl:for-each select="/R/data/prod/technicals/technical">
                   <li><xsl:value-of select="@name"/>: <font color="#C50069"><xsl:value-of select="@val"/></font></li>
                 </xsl:for-each>
               </ul>
             </xsl:if> 
             <!--              <xsl:copy-of select="./discription"><xsl:apply-templates name="copy"/></xsl:copy-of>-->
          </td></tr>
          <tr><td colspan='3' css:padding-top='2px'>
              <!--            <xsl:if test='/R/data/categorys/category'>
              <xsl:element name='a'>
                <xsl:attribute name="href">add2cart?product_id=<xsl:value-of select='@id'/>&#38;path_info=<xsl:value-of select='/R/page/path_encode'/>&#38;opt=<xsl:value-of select='@opt'/></xsl:attribute>
                <xsl:attribute name="class">buy</xsl:attribute>
                <img src='/data/button_sale.png' border='0'/>
              </xsl:element>
            </xsl:if>-->
            <xsl:if test="@metric !=''">



            <font color='red' size='3pt'>Внимание!
            <br/>
            Минимальный заказ составляет <xsl:value-of select='@metric'/></font>
        </xsl:if>
        </td></tr>
      </table>
        <xsl:element name='a'>
          <xsl:attribute name="href"><xsl:value-of select='@path_encode'/></xsl:attribute>
          <xsl:attribute name="class">buy</xsl:attribute>
          Вернуться к списку товаров 
        </xsl:element>
      <xsl:if test="/R/data/more/prod">
        <H4>С этим товаром покупают</H4>
      <div class='week-goods goods'>
        <xsl:for-each select="/R/data/more/prod">
          <p class="center-column-goods" css:width="170px" css:height="230px">
              <xsl:element name='a'>
                <xsl:attribute name="class">category</xsl:attribute>
                <xsl:attribute name="href">product?product_id=<xsl:value-of select='@id'/></xsl:attribute>
                <xsl:value-of select='@name'/>
              </xsl:element>
              <br/>
              <xsl:element name='a'>
        			  <xsl:attribute name="class">thumb</xsl:attribute>
                <xsl:attribute name="href">product?product_id=<xsl:value-of select='@id'/></xsl:attribute>
                <xsl:element name='img'>
                  <xsl:attribute name="alt"><xsl:value-of select='@name'/></xsl:attribute>
                  <xsl:attribute name="title"><xsl:value-of select='@name'/></xsl:attribute>
                  <xsl:attribute name="border">0</xsl:attribute>
                  <xsl:attribute name="src">/<xsl:value-of select='@path'/>/<xsl:value-of select='@photo'/>_small.png</xsl:attribute>
                  <xsl:attribute name="width"><xsl:value-of select='@small_x'/></xsl:attribute>
                  <xsl:attribute name="height"><xsl:value-of select='@small_y'/></xsl:attribute>
                </xsl:element>
              </xsl:element>
          </p>
        </xsl:for-each>
      </div>
      </xsl:if>
    </xsl:for-each>
    <xsl:if test="/R/data/comments/comment">
      <br css:clear="both"/>
      <h3 css:color="#C50069">Отзывы покупателей:</h3>
      <table border='0px'>
        <xsl:for-each select='/R/data/comments/comment'>
          <tr>
            <td><b><xsl:value-of select="@name"/></b>:</td><td><p><xsl:value-of select="@comment"/></p></td>
          </tr>
        </xsl:for-each>
      </table>
    </xsl:if>
    <br/>
    <b>Вы можете оставить отзыв о продукте</b>
  </xsl:template>
  <xsl:template match="copy">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
