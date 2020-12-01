<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <font color='#C50069'><b>Ваша корзина /</b> Оформление заказа</font>
    <h1/> 
    <h3>В вашей корзине</h3>
    <form class='mycart' action="/mycart" method="POST">
      <table class="tsimple mycart" border="1" width="100%">
        <tr class='top'>
          <td class='no left'>Наименование</td>
          <td class='no'>Цена</td>
          <td class='no'>Количество</td>
          <td class='no'>Сумма</td>
          <td class='no right'>Действия
              <xsl:element name="input">
                <xsl:attribute name="type">
                  <xsl:text>hidden</xsl:text>
                </xsl:attribute>
                <xsl:attribute name="name">path</xsl:attribute>
                <xsl:attribute name="value">
                  <xsl:value-of select="/R/data/@path"/>
                </xsl:attribute>
              </xsl:element>
          </td>
        </tr>
        <xsl:for-each select="/R/data/products/product">
          <tr class='good'>
            <td class='left'>
              <xsl:element name="a">
                <xsl:attribute name="href">/product?product_id=<xsl:value-of select="@id"/></xsl:attribute><xsl:value-of select="@name"/>
              </xsl:element>
            </td>
            <td class='black'>
              <xsl:value-of select="@price"/>
            </td>
            <td class='black'>
              <xsl:element name="input">
                <xsl:attribute name="class">docart</xsl:attribute>
                <xsl:attribute name="type">
                  <xsl:text>text</xsl:text>
                </xsl:attribute>
                <xsl:attribute name="name">
                  <xsl:value-of select="@id"/>
                </xsl:attribute>
                <xsl:attribute name="size">
                  <xsl:text>4</xsl:text>
                </xsl:attribute>
                <xsl:attribute name="value">
                  <xsl:value-of select="@count"/>
                </xsl:attribute>
              </xsl:element>
            </td>
            <td class='amount'><xsl:value-of select="@amount"/></td>
            <td class="no right">
              <xsl:element name="a">
                <xsl:attribute name="href">
                  <xsl:value-of select="/R/page/serv_name"/>
                  <xsl:text>/delfromcart?product_id=</xsl:text>
                  <xsl:value-of select="@id"/>
                  <xsl:text>&amp;path_info=</xsl:text>
                  <xsl:value-of select="/R/page/path_encode"/>
                </xsl:attribute>
                <xsl:element name="img">
                  <xsl:attribute name="src">
                    <xsl:value-of select="/R/page/serv_name"/><xsl:text>/del.jpeg</xsl:text>
                  </xsl:attribute>
                  <xsl:attribute name="border">
                    <xsl:text>0</xsl:text>
                  </xsl:attribute>
                  <xsl:attribute name="title">
                    <xsl:text>удалить</xsl:text>
                  </xsl:attribute>
                  <xsl:attribute name="alt">
                    <xsl:text>удалить</xsl:text>
                  </xsl:attribute>
                </xsl:element>
                <xsl:text>удалить</xsl:text>
              </xsl:element>
            </td>
          </tr>
        </xsl:for-each>
        <tr class='my amount-all'>
        	<td colspan='3' class='left_no left'>Сумма заказа без учета бонусов:</td>
        	<td class='no amount'><xsl:value-of select="/R/data/res"/></td>
        	<td class='right'><input type="submit" value="пересчитать"/></td>
        </tr>
        <tr class='my'>
          <td colspan='3' class='left_no attention left'><b>Внимание!</b> Большинство товаров в интернет-магазине имеют большие скидки, действительные только в интернет магазине.</td>
          <td colspan='2' class='no right'><a class='docart' href='/docart'>Оформить заказ</a></td>
        </tr>
      </table>
    </form>
    <xsl:element name="a">
      <xsl:attribute name="href">
        <xsl:value-of select="/R/data/@link"/>
      </xsl:attribute>
      Перейти к списку товаров
    </xsl:element>
    <br/><br/><br/>
    <xsl:for-each select="/R/data/discrs/discr">
      <b><xsl:value-of select="@name"/></b><br/>
      <div class='disc'>
         <xsl:copy-of select="."><xsl:apply-templates name="copy"/></xsl:copy-of>
      </div>
      <br/>
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="copy">
    <xsl:copy>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>

