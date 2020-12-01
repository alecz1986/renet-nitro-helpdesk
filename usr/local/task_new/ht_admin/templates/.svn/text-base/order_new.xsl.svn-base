<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class="tsimple" id="order_table">
      <tr class=" tr_order font-weight">
        <td>номер заказа</td>
        <td>дата </td>
        <td width='70px' css:text-align='center'>статус</td>
        <td width='400px'>заказ</td>
        <td>дата доставки</td>
        <td width='200px'>комментарии</td>
        <td>история</td>
      </tr>
      <xsl:for-each select="/R/data/order">
        <tr class="tr_order">
          <td>
            <xsl:element name="a">
              <xsl:attribute name="href">/private/order/detail?order_id=<xsl:value-of select="./ord_id"/></xsl:attribute>
              <xsl:attribute name="target">_blank</xsl:attribute>
              <xsl:value-of select="./ord_id"/>
            </xsl:element>
            <br/>
            <xsl:element name="a">
              <xsl:attribute name="href">/private/order_print?order_id=<xsl:value-of select="./ord_id"/></xsl:attribute>
              <xsl:attribute name="target">_blank</xsl:attribute>
              печать
            </xsl:element>
          </td>
          <td class="nowrap"><xsl:value-of select="./dt"/></td>
          <td class="nowrap">
            <xsl:element name="em">
              <xsl:attribute name="class"> stat ajax status<xsl:value-of select="./stid"/></xsl:attribute>
              <xsl:attribute name="order_id"><xsl:value-of select="./ord_id"/></xsl:attribute>
                <xsl:value-of select="./status"/>
            </xsl:element>
          </td>
          <td>
            <em><b>ФИО:</b> <xsl:value-of select="./fio"/></em><br/>
            <em><b>адрес:</b> <xsl:value-of select="./address"/></em><br/>
            <em><b>телефон:</b> <xsl:value-of select="./phones"/></em><br/>
            <em><b>email:</b> <xsl:value-of select="./email"/></em><br/>
            <em><b>доставка:</b> <xsl:value-of select="./delivery"/></em><br/>
            <em><b>оплата:</b> <xsl:value-of select="./pmt"/></em><br/>
            <em><b>комментарий:</b><xsl:value-of select="./note"/></em><br/><br/>
            <em><b>скидка:</b></em>
            <xsl:element name="em">
              <xsl:value-of select="./sale"/>
            </xsl:element>
            <br/><br/>
            <p>
              <xsl:for-each select="./prods/prod">
                <xsl:element name="em"> 
                 <xsl:if test="./@close='yes'">
                    <xsl:attribute name="class">line-through</xsl:attribute>
                 </xsl:if>
                 <xsl:value-of select="./@name"/> (<font class='red'><xsl:value-of select="./@count"/></font>) цена <xsl:value-of select="./@amount"/>р.
                </xsl:element><br/>
             </xsl:for-each>
            </p><br/>

            <b>ИТОГО: 
              <xsl:element name="font">
                <xsl:attribute name="class">red</xsl:attribute>
                <xsl:attribute name="id">font<xsl:value-of select="./ord_id"/></xsl:attribute>
                <xsl:value-of select="./amount"/>
              </xsl:element>
            </b><br/>
          </td>
          <xsl:element name="td">
            <xsl:attribute name="id">td<xsl:value-of select="./ord_id"/></xsl:attribute>
            <xsl:attribute name="order_id"><xsl:value-of select="./ord_id"/></xsl:attribute>
            <xsl:attribute name="class">dt_distr nowrap ajax <xsl:value-of select="./dt_distr/@css"/></xsl:attribute>
            <xsl:value-of select="./dt_distr"/>
          </xsl:element>
          <td>
            <xsl:element name="em">
            <xsl:attribute name="class">ajax comment blue</xsl:attribute>
            <xsl:attribute name="order_id"><xsl:value-of select="./ord_id"/></xsl:attribute>
              добавить комментарий
            </xsl:element>
            <br/>
            <xsl:for-each select="./comments/comment">
              <p>
                <xsl:value-of select="./text()"/>   (<xsl:value-of select="./@name"/>)<br/>
              </p>
              <br/>
            </xsl:for-each>
          </td>
          <td>
            <xsl:for-each select="./history/st">
              <p class="nowrap">
                <xsl:value-of select="./@name"/> - <xsl:value-of select="./@oper"/>   (<xsl:value-of select="./@dt"/>)
              </p>
            </xsl:for-each>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <xsl:if test="/R/data/@prev != ''">
      <xsl:element name="a">
        <xsl:attribute name="href">/private/order?status=<xsl:value-of select="/R/data/@status"/>&#38;offset=<xsl:value-of select="/R/data/@prev"/>&#38;date_b=<xsl:value-of select="/R/data/@date_b"/>&#38;date_e=<xsl:value-of select="/R/data/@date_e"/></xsl:attribute>
        <xsl:text>назад</xsl:text>
      </xsl:element>
    </xsl:if>
    <xsl:if test="/R/data/@next != ''">
      <xsl:element name="a">
        <xsl:attribute name="href">/private/order?status=<xsl:value-of select="/R/data/@status"/>&#38;offset=<xsl:value-of select="/R/data/@next"/>&#38;date_b=<xsl:value-of select="/R/data/@date_b"/>&#38;date_e=<xsl:value-of select="/R/data/@date_e"/></xsl:attribute>
        <xsl:text>вперед</xsl:text>
      </xsl:element>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>

