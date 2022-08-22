# Data Masking

This feature was implemented in *Percona Server for MySQL* version Percona Server for MySQL 5.7.32-35.

The Percona Data Masking plugin is a free and Open Source implementation of the
MySQL’s data masking plugin. Data Masking provides a set of functions to hide
sensitive data with modified content.

Data masking can have either of the characteristics:

* Generation of random data, such as an email address

* De-identify data by transforming the data to hide content

### Installing the plugin

The following command installs the plugin:

```sql
mysql> INSTALL PLUGIN data_masking SONAME 'data_masking.so';
```

### Data Masking functions

The data masking functions have the following categories:

* General purpose

* Special purpose

* Generating Random Data with Defined characteristics

* Using Dictionaries to Generate Random Data

### General Purpose

The general purpose data masking functions are the following:

<table class="colwidths-given docutils align-default">
<colgroup>
<col style="width: 18%" />
<col style="width: 27%" />
<col style="width: 55%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Parameter</p></th>
<th class="head"><p>Description</p></th>
<th class="head"><p>Sample</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>mask_inner(string, margin1, margin2 [, character])</p></td>
<td><p>Returns a result where only the inner part of a string is masked. An
optional masking character can be specified.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">mask_inner</span><span class="p">(</span><span class="s1">&#39;123456789&#39;</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">);</span>

<span class="o">+-----------------------------------+</span>
<span class="o">|</span> <span class="nf">mask_inner</span><span class="p">(</span><span class="s2">&quot;123456789&quot;</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">)</span>     <span class="o">|</span>
<span class="o">+-----------------------------------+</span>
<span class="o">|</span><span class="mi">1</span><span class="n">XXXXXX89</span>                          <span class="o">|</span>
<span class="o">+-----------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
<tr class="row-odd"><td><p>mask_outer(string, margin1, margin2 [, character])</p></td>
<td><p>Masks the outer part of the string. The inner section is not masked.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">mask_outer</span><span class="p">(</span><span class="s1">&#39;123456789&#39;</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">2</span><span class="p">);</span>

<span class="o">+------------------------------------+</span>
<span class="o">|</span> <span class="nf">mask_outer</span><span class="p">(</span><span class="s2">&quot;123456789&quot;</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">2</span><span class="p">).</span>     <span class="o">|</span>
<span class="o">+------------------------------------+</span>
<span class="o">|</span> <span class="n">XX34567XX</span>                          <span class="o">|</span>
<span class="o">+------------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
</tbody>
</table>



### Special Purpose

The special purpose data masking functions are as follows:

### Generating Random Data for Specific Requirements

The following functions generate random values for specific requirements:

<table class="colwidths-given docutils align-default">
<colgroup>
<col style="width: 18%" />
<col style="width: 27%" />
<col style="width: 55%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Parameter</p></th>
<th class="head"><p>Description</p></th>
<th class="head"><p>Sample</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>gen_range(lower, upper)</p></td>
<td><p>Generates a random number based on a selected range and supports
negative numbers.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_range</span><span class="p">(</span><span class="mi">10</span><span class="p">,</span> <span class="mi">100</span><span class="p">)</span> <span class="k">AS</span> <span class="n">result</span><span class="p">;</span>

<span class="o">+--------------------------------------+</span>
<span class="o">|</span> <span class="n">result</span>                               <span class="o">|</span>
<span class="o">+--------------------------------------+</span>
<span class="o">|</span> <span class="mi">56</span>                                   <span class="o">|</span>
<span class="o">+--------------------------------------+</span>

<span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_range</span><span class="p">(</span><span class="mi">100</span><span class="p">,</span><span class="mi">80</span><span class="p">);</span>

<span class="o">+--------------------------------------+</span>
<span class="o">|</span> <span class="nf">gen_range</span><span class="p">(</span><span class="mi">100</span><span class="p">,</span><span class="mi">80</span><span class="p">)</span>                    <span class="o">|</span>
<span class="o">+--------------------------------------+</span>
<span class="o">|</span> <span class="mi">91</span>                                   <span class="o">|</span>
<span class="o">+--------------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
<tr class="row-odd"><td><p>gen_rnd_email()</p></td>
<td><p>Generates a random email address. The domain is <code class="docutils literal notranslate"><span class="pre">example.com</span></code>.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_rnd_email</span><span class="p">();</span>

<span class="o">+---------------------------------------+</span>
<span class="o">|</span> <span class="nf">gen_rnd_email</span><span class="p">()</span>                       <span class="o">|</span>
<span class="o">+---------------------------------------+</span>
<span class="o">|</span> <span class="n">sma</span><span class="p">.</span><span class="n">jrts</span><span class="o">@</span><span class="n">example</span><span class="p">.</span><span class="n">com</span>                  <span class="o">|</span>
<span class="o">+---------------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
<tr class="row-even"><td><p>gen_rnd_pan([size in integer])</p></td>
<td><p>Generates a random primary account number. This function should only
be used for test purposes.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">mask_pan</span><span class="p">(</span><span class="nf">gen_rnd_pan</span><span class="p">());</span>

<span class="o">+-------------------------------------+</span>
<span class="o">|</span> <span class="nf">mask_pan</span><span class="p">(</span><span class="nf">gen_rnd_pan</span><span class="p">())</span>             <span class="o">|</span>
<span class="o">+-------------------------------------+</span>
<span class="o">|</span> <span class="n">XXXXXXXXXXXX4444</span>                    <span class="o">|</span>
<span class="o">+-------------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
<tr class="row-odd"><td><p>gen_rnd_us_phone()</p></td>
<td><p>Generates a random U.S. phone number. The generated number adds the
<cite>1</cite> dialing code and is in the <cite>555</cite> area code. The <cite>555</cite> area code
is not valid for any U.S. phone number.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_rnd_us_phone</span><span class="p">();</span>

<span class="o">+-------------------------------+</span>
<span class="o">|</span> <span class="nf">gen_rnd_us_phone</span><span class="p">()</span>            <span class="o">|</span>
<span class="o">+-------------------------------+</span>
<span class="o">|</span> <span class="mi">1</span><span class="o">-</span><span class="mi">555</span><span class="o">-</span><span class="mi">635</span><span class="o">-</span><span class="mi">5709</span>                <span class="o">|</span>
<span class="o">+-------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
<tr class="row-even"><td><p>gen_rnd_ssn()</p></td>
<td><p>Generates a random, non-legitimate US Social Security Number in
an <code class="docutils literal notranslate"><span class="pre">AAA-BBB-CCCC</span></code> format. This function should only be used for test
purposes.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_rnd_ssn</span><span class="p">()</span>

<span class="o">+-----------------------------+</span>
<span class="o">|</span> <span class="nf">gen_rnd_ssn</span><span class="p">()</span>               <span class="o">|</span>
<span class="o">+-----------------------------+</span>
<span class="o">|</span> <span class="mi">995</span><span class="o">-</span><span class="mi">33</span><span class="o">-</span><span class="mi">5656</span>                 <span class="o">|</span>
<span class="o">+-----------------------------+</span>
</pre></div>
</div>
</td>
</tr>
</tbody>
</table>

### Using Dictionaries to Generate Random Terms

Data masking returns a value from a range. To use a predefined file as the range to select a string value, load and use a dictionary. A dictionary supports only strings and is loaded from a file with the following characteristics:


* Plain text


* One term per line


* Must contain at least one entry

An example of a dictionary, which is a list of trees, located in /usr/local/mysql/dict-files/testdict


* Black Ash


* White Ash


* Bigtooth Aspen


* Quaking Aspen

The following table displays the commands for using dictionaries to generate random terms:

<table class="colwidths-given docutils align-default">
<colgroup>
<col style="width: 18%" />
<col style="width: 27%" />
<col style="width: 55%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Parameter</p></th>
<th class="head"><p>Description</p></th>
<th class="head"><p>Sample</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>gen_range(lower, upper)</p></td>
<td><p>Generates a random number based on a selected range and supports
negative numbers.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_range</span><span class="p">(</span><span class="mi">10</span><span class="p">,</span> <span class="mi">100</span><span class="p">)</span> <span class="k">AS</span> <span class="n">result</span><span class="p">;</span>

<span class="o">+--------------------------------------+</span>
<span class="o">|</span> <span class="n">result</span>                               <span class="o">|</span>
<span class="o">+--------------------------------------+</span>
<span class="o">|</span> <span class="mi">56</span>                                   <span class="o">|</span>
<span class="o">+--------------------------------------+</span>

<span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_range</span><span class="p">(</span><span class="mi">100</span><span class="p">,</span><span class="mi">80</span><span class="p">);</span>

<span class="o">+--------------------------------------+</span>
<span class="o">|</span> <span class="nf">gen_range</span><span class="p">(</span><span class="mi">100</span><span class="p">,</span><span class="mi">80</span><span class="p">)</span>                    <span class="o">|</span>
<span class="o">+--------------------------------------+</span>
<span class="o">|</span> <span class="mi">91</span>                                   <span class="o">|</span>
<span class="o">+--------------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
<tr class="row-odd"><td><p>gen_rnd_email()</p></td>
<td><p>Generates a random email address. The domain is <code class="docutils literal notranslate"><span class="pre">example.com</span></code>.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_rnd_email</span><span class="p">();</span>

<span class="o">+---------------------------------------+</span>
<span class="o">|</span> <span class="nf">gen_rnd_email</span><span class="p">()</span>                       <span class="o">|</span>
<span class="o">+---------------------------------------+</span>
<span class="o">|</span> <span class="n">sma</span><span class="p">.</span><span class="n">jrts</span><span class="o">@</span><span class="n">example</span><span class="p">.</span><span class="n">com</span>                  <span class="o">|</span>
<span class="o">+---------------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
<tr class="row-even"><td><p>gen_rnd_pan([size in integer])</p></td>
<td><p>Generates a random primary account number. This function should only
be used for test purposes.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">mask_pan</span><span class="p">(</span><span class="nf">gen_rnd_pan</span><span class="p">());</span>

<span class="o">+-------------------------------------+</span>
<span class="o">|</span> <span class="nf">mask_pan</span><span class="p">(</span><span class="nf">gen_rnd_pan</span><span class="p">())</span>             <span class="o">|</span>
<span class="o">+-------------------------------------+</span>
<span class="o">|</span> <span class="n">XXXXXXXXXXXX4444</span>                    <span class="o">|</span>
<span class="o">+-------------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
<tr class="row-odd"><td><p>gen_rnd_us_phone()</p></td>
<td><p>Generates a random U.S. phone number. The generated number adds the
<cite>1</cite> dialing code and is in the <cite>555</cite> area code. The <cite>555</cite> area code
is not valid for any U.S. phone number.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_rnd_us_phone</span><span class="p">();</span>

<span class="o">+-------------------------------+</span>
<span class="o">|</span> <span class="nf">gen_rnd_us_phone</span><span class="p">()</span>            <span class="o">|</span>
<span class="o">+-------------------------------+</span>
<span class="o">|</span> <span class="mi">1</span><span class="o">-</span><span class="mi">555</span><span class="o">-</span><span class="mi">635</span><span class="o">-</span><span class="mi">5709</span>                <span class="o">|</span>
<span class="o">+-------------------------------+</span>
</pre></div>
</div>
</td>
</tr>
<tr class="row-even"><td><p>gen_rnd_ssn()</p></td>
<td><p>Generates a random, non-legitimate US Social Security Number in
an <code class="docutils literal notranslate"><span class="pre">AAA-BBB-CCCC</span></code> format. This function should only be used for test
purposes.</p></td>
<td><div class="highlight-MySQL notranslate"><div class="highlight"><pre><span></span><span class="n">mysql</span><span class="o">&gt;</span> <span class="k">SELECT</span> <span class="nf">gen_rnd_ssn</span><span class="p">()</span>

<span class="o">+-----------------------------+</span>
<span class="o">|</span> <span class="nf">gen_rnd_ssn</span><span class="p">()</span>               <span class="o">|</span>
<span class="o">+-----------------------------+</span>
<span class="o">|</span> <span class="mi">995</span><span class="o">-</span><span class="mi">33</span><span class="o">-</span><span class="mi">5656</span>                 <span class="o">|</span>
<span class="o">+-----------------------------+</span>
</pre></div>
</div>
</td>
</tr>
</tbody>
</table>

### Uninstalling the plugin

The [UNINSTALL PLUGIN](https://dev.mysql.com/doc/refman/5.7/en/uninstall-plugin.html) statement disables and uninstalls the plugin.
