<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
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
    <div css:padding-left="10px;" align='center'>
      <xsl:if test="/R/data/@photo">
        <xsl:element name='img'>
          <xsl:attribute name='src'><xsl:value-of select='/R/page/serv/@name'/>category/<xsl:value-of select='/R/data/@photo'/></xsl:attribute>
          <xsl:attribute name='border'>0</xsl:attribute>
          <xsl:attribute name='width'>200</xsl:attribute>
        </xsl:element>
      </xsl:if>
      <br/>
    </div>
    <a href='/' css:color="#C50069" css:font-weight="bold">Каталог</a>
    <xsl:for-each select="/R/data/categorys/category">
      <xsl:text> / </xsl:text>
      <xsl:element name='a'>
        <xsl:attribute name='href'>/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select="@id"/></xsl:attribute>
        <xsl:value-of select="@name"/>
      </xsl:element>
    </xsl:for-each>
    <br/>
    <ul class='menu' width='500px'>
      <xsl:for-each select="/R/data/last_click/category">
        <li>
          <xsl:element name='a'>
            <xsl:attribute name='href'>/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select="@id"/></xsl:attribute>
            <xsl:value-of select="@name"/>
          </xsl:element>
        </li>
      </xsl:for-each>
      <xsl:for-each select="/R/data/categorys_link/category">
        <li>
          <xsl:element name='a'>
            <xsl:attribute name='href'>/<xsl:value-of select='@template'/>?category_id=<xsl:value-of select="@link"/></xsl:attribute>
            <xsl:value-of select="@name"/>
          </xsl:element>
          <br/>
        </li>
      </xsl:for-each>
    </ul>
    <br css:clear="both"/>
    <h1/>
    <font color="red" size="2">
       <xsl:if test="/R/data/@warning != 'None'">
        <xsl:value-of select="/R/data/@warning"/>
       </xsl:if>
    </font>
    <br/>
    <xsl:copy-of select="/R/data/discription/*"><xsl:apply-templates name="copy"/></xsl:copy-of>
    <br/>
    <form action='/category_opt' method='get'>
      <xsl:element name="input">
        <xsl:attribute name="name"><xsl:text>category_id</xsl:text></xsl:attribute>
        <xsl:attribute name="type"><xsl:text>hidden</xsl:text></xsl:attribute>
        <xsl:attribute name="value"><xsl:value-of select="/R/data/@category_id"/></xsl:attribute>
      </xsl:element>
      <xsl:element name="input">
        <xsl:attribute name="name"><xsl:text>page</xsl:text></xsl:attribute>
        <xsl:attribute name="type">hidden</xsl:attribute>
        <xsl:attribute name="value"><xsl:value-of select="/R/data/@page"/></xsl:attribute>
      </xsl:element>
      <xsl:if test="/R/data/@auto = '0'">
        <xsl:element name="input">
          <xsl:attribute name="name"><xsl:text>price</xsl:text></xsl:attribute>
          <xsl:attribute name="type"><xsl:text>radio</xsl:text></xsl:attribute>
          <xsl:attribute name="id"><xsl:text>radio1</xsl:text></xsl:attribute>
          <xsl:if test="/R/data/@price = 'asc' ">
            <xsl:attribute name="checked">true</xsl:attribute>
          </xsl:if>
          <xsl:attribute name="value"><xsl:text>asc</xsl:text></xsl:attribute>
          <xsl:attribute name="onClick"><xsl:text>this.form.submit()</xsl:text></xsl:attribute>
          <label for="radio1"><xsl:text>отсортировать цены по возрастанию</xsl:text></label>
        </xsl:element>
        <br/>
        <xsl:element name="input">
          <xsl:attribute name="name"><xsl:text>price</xsl:text></xsl:attribute>
          <xsl:attribute name="type"><xsl:text>radio</xsl:text></xsl:attribute>
          <xsl:attribute name="id"><xsl:text>radio2</xsl:text></xsl:attribute>
          <xsl:if test="/R/data/@price = 'desc' ">
            <xsl:attribute name="checked">true</xsl:attribute>
          </xsl:if>
          <xsl:attribute name="value"><xsl:text>desc</xsl:text></xsl:attribute>
          <xsl:attribute name="onClick"><xsl:text>this.form.submit()</xsl:text></xsl:attribute>
          <label for="radio2"><xsl:text>отсортировать цены по убыванию</xsl:text></label>
        </xsl:element>
        <br/>
                          <xsl:element name="select">
                    <xsl:attribute name="name">show</xsl:attribute>
                    <xsl:attribute name="id">show</xsl:attribute>
                    <xsl:attribute name="onChange"><xsl:text>this.form.submit()</xsl:text></xsl:attribute>
                    <xsl:for-each select="/R/data/options/option">
                      <xsl:element name="option">
                        <xsl:attribute name="value"><xsl:value-of select="@value"/></xsl:attribute>
                        <xsl:if test="@sel='1'"><xsl:attribute name="selected"></xsl:attribute></xsl:if>
                        <xsl:value-of select="@value"/>
                      </xsl:element>
                    </xsl:for-each>
                  </xsl:element>
          <label for="show"><xsl:text> товаров на странице</xsl:text></label>
      </xsl:if>
    </form>
    <xsl:if test='/R/data/spec/sp'>
      <h1>Специальные предложения</h1>
    </xsl:if>
    <div class='week-goods goods'>
      <xsl:for-each select="/R/data/spec/sp">
        <p css:width="400px">
          <xsl:element name='a'>
            <xsl:attribute name="href"><xsl:value-of select='@template'/>?category_id=<xsl:value-of select='@cat_id'/></xsl:attribute>
            <xsl:attribute name="class">category</xsl:attribute>
            <xsl:value-of select='@cat_name'/>
          </xsl:element>
          <xsl:element name='a'>
            <xsl:attribute name="href">product?product_id=<xsl:value-of select='@id'/><xsl:text>&amp;path=</xsl:text><xsl:value-of select='/R/page/path_encode'/></xsl:attribute>
            <xsl:element name='img'>
              <xsl:attribute name="alt"><xsl:value-of select='@name'/></xsl:attribute>
              <xsl:attribute name="title"><xsl:value-of select='@name'/></xsl:attribute>
              <xsl:attribute name="src"><xsl:value-of select='/R/page/serv/@name'/>
                <xsl:value-of select='@path'/>
                <xsl:text>/</xsl:text>
                <xsl:value-of select='@photo'/>
                <xsl:text>_small.png</xsl:text>
              </xsl:attribute>
              <xsl:attribute name="width"><xsl:value-of select='@small_x'/></xsl:attribute>
              <xsl:attribute name="height"><xsl:value-of select='@small_y'/></xsl:attribute>
            </xsl:element>
          </xsl:element>
          <xsl:if test="@holiday = 'yes'">
                    <xsl:element name='a'>
                      <xsl:attribute name='href'>http://peshca.ru/news?new_id=water</xsl:attribute>
                      <xsl:element name='img'>
                        <xsl:attribute name='src'>/ng_small.png</xsl:attribute>
                        <xsl:attribute name="border">0</xsl:attribute>
                        <xsl:attribute name="css:margin-left"><xsl:value-of select="@small_x"/>px</xsl:attribute>
                        <xsl:attribute name="class">ng</xsl:attribute>
                      </xsl:element>
                    </xsl:element>
          </xsl:if>
          <b>
            <xsl:element name="a">
              <xsl:attribute name="href">
                <xsl:value-of select="/R/page/serv_name"/><xsl:text>/product?product_id=</xsl:text><xsl:text>&amp;path=</xsl:text><xsl:value-of select='/R/page/path_encode'/><xsl:value-of select="@id"/>
              </xsl:attribute>
              <xsl:value-of select='@name'/>
            </xsl:element>
          </b>
          <em css:font-size="10px">
            <xsl:value-of select='overview'/>
          </em>
          <span class='price'>
            <xsl:value-of select='@price'/>
            <xsl:text>.-</xsl:text>
          </span>
          <xsl:element name='a'>
            <xsl:attribute name="href">
              <xsl:text>add2cart?product_id=</xsl:text>
              <xsl:value-of select='@id'/>
              <xsl:text>&#38;path_info=</xsl:text>
              <xsl:value-of select='/R/page/path_encode'/>
            </xsl:attribute>
            <xsl:attribute name="class">buy</xsl:attribute>
            <xsl:text>купить</xsl:text>
          </xsl:element>
        </p>  
      </xsl:for-each>
    </div>
    <div>
      <h1><xsl:value-of select="/R/data/@cat_name"/></h1>
      <form class='mycart' action="/add2cart" method="GET">
       <div css:float='none' css:text-align='center'>
         <input type="submit" value="купить"/>
       </div>
         <xsl:for-each select="/R/data/products/product">
            <p css:width="500px" css:float='left' css:margin='5px' css:height='60px' class='my'>
                  <xsl:element name='a'>
                    <xsl:attribute name="css:width">100px</xsl:attribute>
                    <xsl:attribute name="css:height">60px</xsl:attribute>
                    <xsl:attribute name="css:float">left</xsl:attribute>
                    <xsl:attribute name='href'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="./photo/@path"/>/<xsl:value-of select="./photo/@photo"/>.png</xsl:attribute>
                    <xsl:attribute name='onclick'>return hs.expand(this,
                          {wrapperClassName: 'borderless floating-caption', dimmingOpacity: 0.75, align: 'center'})</xsl:attribute>
                    <xsl:element name='img'>
                      <xsl:attribute name='src'><xsl:value-of select='/R/page/serv/@name'/><xsl:value-of select="./photo/@path"/>/<xsl:value-of select="./photo/@photo"/>_small.png</xsl:attribute>
                      <xsl:attribute name="border">0</xsl:attribute>
                      <xsl:attribute name="width"><xsl:value-of select='./photo/@small_x'/></xsl:attribute>
                      <xsl:attribute name="height"><xsl:value-of select='./photo/@small_y'/></xsl:attribute>
                      <xsl:attribute name="alt"><xsl:value-of select="@name"/></xsl:attribute>
                    </xsl:element>
                  </xsl:element>
	              <em class='my' css:border-left='1px solid  #C5C5C5' css:border-right='1px solid  #C5C5C5' css:padding='0 5px' css:width='140px' css:float='left' css:height='60px'  css:margin='0px'>
                 <xsl:element name="a">
                   <xsl:attribute name="href">/product?product_id=<xsl:value-of select="@id"/><xsl:text>&amp;path=</xsl:text><xsl:value-of select='/R/page/path_encode'/></xsl:attribute>
                   <font css:font-size="10px" css:color='#353535'><xsl:value-of select="@name"/></font>
                 </xsl:element>
                 <br/>
                 <font css:font-size='9px' css:margin-right="5px" css:font-family="Arial" css:font-weight="normal" css:font-style="normal">
                   <xsl:value-of select='overview'/>
                 </font>
               </em>
	             <em class='my' css:border='0px' css:padding='0 5px' css:width='50px' css:float='left' css:height='60px'  css:margin='0px' css:border-right='1px solid  #C5C5C5'>
                <span css:margin-left='2px'>
                  <xsl:value-of select="@metric"/>
                </span>
               </em>
	             <em class='my' css:padding='0 5px' css:width='140px' css:height='60px'  css:margin='0px' css:font-size='8px'>
                 <span class="price" css:font-size='11px'>
                   <xsl:value-of select="@price"/>
                   <xsl:text>.</xsl:text>
                 </span>
                 <br/>
                 <xsl:element name='input'>
                   <xsl:attribute name='size'>3</xsl:attribute>
                   <xsl:attribute name='type'>text</xsl:attribute>
                   <xsl:attribute name='value'><xsl:value-of select="@ct"/></xsl:attribute>
                   <xsl:attribute name='id'><xsl:value-of select="@id"/></xsl:attribute>
                   <xsl:attribute name='onchange'>add2cart(<xsl:value-of select="@id"/>)</xsl:attribute>
                   <xsl:attribute name='css:margin-left'>2px</xsl:attribute>
                </xsl:element>
                <span css:margin-left='2px'>
                  <xsl:value-of select="@metric"/>
                </span>
               </em>
               <!--               <td class='left_no' width='50px'>
                                  <xsl:element name="a" class='buy'>
                   <xsl:attribute name="class">buy</xsl:attribute>
                   <xsl:attribute name="href">
                     <xsl:text>/add2cart?product_id=</xsl:text>
                     <xsl:value-of select="@id"/>
                     <xsl:text>&#38;path_info=</xsl:text>
                     <xsl:value-of select='/R/page/path_encode'/>
                   </xsl:attribute>
                   <xsl:text>купить</xsl:text>
                 </xsl:element>
               </td>-->
         </p>
       </xsl:for-each>
       <div css:float='none' css:text-align='center' css:clear='both'>
         <input type="hidden" value="" id='res' name='res'/><input type="hidden" value="1"  name='opt'/><input type="submit" value="купить"/>
         <xsl:element name='input'>
           <xsl:attribute name='type'>hidden</xsl:attribute>
           <xsl:attribute name='name'>path_info</xsl:attribute>
           <xsl:attribute name='value'><xsl:value-of select='/R/page/path_encode'/></xsl:attribute>
         </xsl:element>
       </div>
    </form>
    <xsl:if test='/R/data/pages/page'>
      <h1 css:clear='both'>Страницы:</h1>
    </xsl:if>
    <xsl:value-of select='/R/data/pages/prev/@val'/>
    <xsl:for-each select="/R/data/pages/page">
      <xsl:choose>
        <xsl:when test='@action = "1"'>
          <b css:color='#C50069'><xsl:value-of select='@val'/></b>
          <xsl:text>&#160;  &#160;</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:element name="a">
            <xsl:choose>
              <xsl:when test='@id'>
                <xsl:attribute name="href">/category_opt?category_id=<xsl:value-of select='@id'/>&#38;page=<xsl:value-of select='@val'/>&#38;price=<xsl:value-of select='/R/data/@price'/>&#38;show=<xsl:value-of select='/R/data/@show'/></xsl:attribute>
              </xsl:when>
              <xsl:otherwise>
                <xsl:attribute name="href">/searchstring?s=<xsl:value-of select='/R/data/@s'/>&#38;page=<xsl:value-of select='@val'/>&#38;price=<xsl:value-of select='/R/data/@price'/>&#38;w=<xsl:value-of select='/R/data/@w'/>&#38;h=<xsl:value-of select='/R/data/@h'/>&#38;d=<xsl:value-of select='/R/data/@d'/>&#38;mark=<xsl:value-of select='/R/data/@mark'/>&#38;show=<xsl:value-of select='/R/data/@show'/></xsl:attribute>
              </xsl:otherwise>
            </xsl:choose>
            <xsl:value-of select='@val'/>
          </xsl:element>  
          <xsl:text>&#160;  &#160;</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:value-of select='/R/data/pages/next/@val'/>
  </div>
  <br css:clear="both"/>
  </xsl:template>
  <xsl:template match="copy">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
