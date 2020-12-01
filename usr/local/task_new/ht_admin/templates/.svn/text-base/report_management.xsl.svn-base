<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <script>
      var params='<xsl:for-each  select='/R/data/gets/*'><xsl:value-of select='name()'/>=<xsl:value-of select='@value'/>&amp;</xsl:for-each>'
      var checks='<xsl:for-each  select='/R/data/params/param'><xsl:if test='@check ="1"'><xsl:value-of select='@count'/>-</xsl:if></xsl:for-each>'
      var _names='<xsl:for-each  select='/R/data/params/param'><xsl:if test='@check ="1"'><xsl:value-of select='@value'/>-</xsl:if></xsl:for-each>'
    </script>
    <form method='post' action='./management' name='f' enctype='multipart/form-data'>
        <div  css:width='100%'  align='center' css:margin='10px'>
          <xsl:element name='input'>
            <xsl:attribute name='type'>text</xsl:attribute>
            <xsl:attribute name='name'>date_begin</xsl:attribute>
            <xsl:attribute name='value'><xsl:value-of select='/R/data/gets/date_begin/@value'/></xsl:attribute>
            <xsl:attribute name='id'>se.date_begin</xsl:attribute>
          </xsl:element>
        <label for='se.date_begin'>Начало периода</label>  
        <input width="20" type="submit" value="#" id="triggerdate_begin" />
          <script type="text/javascript">
            Calendar.setup({
             inputField     :    "se.date_begin",
             ifFormat       :    "%Y-%m-%d",
             button         :    "triggerdate_begin",
             align          :    "Tl",
             singleClick    :    true
            });
          </script>
          <xsl:element name='input'>
            <xsl:attribute name='type'>text</xsl:attribute>
            <xsl:attribute name='name'>date_end</xsl:attribute>
            <xsl:attribute name='value'><xsl:value-of select='/R/data/gets/date_end/@value'/></xsl:attribute>
            <xsl:attribute name='id'>se.date_end</xsl:attribute>
          </xsl:element>
        <label for='se.date_end'>Начало периода</label>  
        <input width="20" type="submit" value="#" id="triggerdate_end" />
           <script type="text/javascript">
              Calendar.setup({
               inputField     :    "se.date_end",
               ifFormat       :    "%Y-%m-%d",
               button         :    "triggerdate_end",
               align          :    "Tl",
               singleClick    :    true
              });
            </script>
        <br/>
        <br/>
        <xsl:for-each select='/R/data/params/param'>
          <xsl:element name='input'>
            <xsl:attribute name='type'>checkbox</xsl:attribute>
            <xsl:attribute name='name'><xsl:value-of select='@name'/></xsl:attribute>
            <xsl:attribute name='class'>opt</xsl:attribute>
            <xsl:attribute name='value'><xsl:value-of select='@name'/></xsl:attribute>
            <xsl:attribute name='id'>opt<xsl:value-of select='@name'/></xsl:attribute>
            <xsl:if test='@check = "1"'>
              <xsl:attribute name='checked'><xsl:value-of select='@check'/></xsl:attribute>
            </xsl:if>

          </xsl:element>
          <xsl:element name='label'>
            <xsl:attribute name='for'>opt<xsl:value-of select='@name'/></xsl:attribute>
            <xsl:attribute name='css:color'><xsl:value-of select='@color'/></xsl:attribute>
            <xsl:value-of select='@value'/>
          </xsl:element>
        </xsl:for-each>
        <br/>
        <br/>
        <label for='file'>Файл для построения</label>  
        <input type="file" value="" id="file" name='csv'/>
        <br/>
        <br/>
        <input type='submit' value='Построить'/>
      </div>
   </form>
   <div id="my-timeplot" css:height="400px;" onMouseMove='show_values()'></div>
    <div id='val' css:visibility='hidden' css:position='absolute' css:top='700px' css:border='1px;opacity:50%'></div>
  </xsl:template>
</xsl:stylesheet>

