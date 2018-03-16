"""Stores all the helper functions that generate html"""
import random

def generate_2choice_html(example):
  '''Makes html for ranking form for the specified row index.
  
  Returns the HTML for a table of radio buttons used for ranking, 
  as well as a count of the total number of radio buttons.
  '''

  # Check for duplicates.
  if example.target_lines[0] == example.target_lines[1]:
    return "", 0

  # Find all the non-duplicate target indices.
  target_indices = [0, 1]

  # Randomize the order targets are shown in.
  random.shuffle(target_indices)
  num_targets = len(target_indices)

  html = """
      <br/>
      <div class="panel panel-default btn-group">
      <h4>Speaker A: %s</h4>
      <table>
      <tr>
      <th align="center">Which is best?</th>
      <th></th>
      </tr>
      """ % example.source_line

  html += """
      <tr>
      <td>Speaker B: %s</td>""" % (example.target_lines[target_indices[0]])
  html += """
      <td>
        <label class="btn">
          <input type="radio" class="%s" name="%s-target-%s" data-col="1" value="1"/>
        </label>
      </td>
      </tr>""" % (example.key, example.key, target_indices[0])

  html += """
      <tr>
      <td>Speaker C: %s</td>""" % (example.target_lines[target_indices[1]])
  html += """
      <td>
        <label class="btn">
          <input type="radio" class="%s" name="%s-target-%s" data-col="1" value="1"/>
        </label>
      </td>
      </tr>""" % (example.key, example.key, target_indices[1])

  html += """
      <tr>
      <td>It's a tie.</td>
      <td>
        <label class="btn">
          <input type="radio" class="%s" name="%s-target-tie" data-col="1" value="1"/>
        </label>
      </td>
      </tr>""" % (example.key, example.key)

  html += """
      </table>
      </div>
      """
  return html, 1




def generate_ranking_tables_html(example):
  '''Makes html for ranking form for the specified row index.
  
  Returns the HTML for a table of radio buttons used for ranking, 
  as well as a count of the total number of radio buttons.
  '''


  # Find all the non-duplicate target indices.
  target_indices = []
  for idx in range(len(example.target_lines)):
    current = example.target_lines[idx]
    if current not in example.target_lines[0:idx] or idx == 0:
      target_indices.append(idx)

  # Randomize the order targets are shown in.
  random.shuffle(target_indices)
  num_targets = len(target_indices)

  html = """
      <br/>
      <div class="panel panel-default btn-group">
      <h4>Speaker A: %s</h4>
      <table>
      <tr>
      <th></th>
      """ % example.source_line

  for idx in range(num_targets):
    if idx == 0:
      tag = 'best'
    elif idx == num_targets - 1:
      tag = 'worst'
    else:
      tag = ''
    html += '<th align="center">%s<br>%s</th>' % (tag, idx+1)
  html += "</tr>"

  for idx in target_indices:
    html += """
        <tr>
        <td>Speaker B: %s</td>""" % (example.target_lines[idx])

    # Add a row of radio buttons whose length is the number of options.
    for jdx in range(num_targets):
      html += """
          <td>
            <label class="btn">
              <input type="radio" class="%s" name="%s-target-%s" data-col="%s" value="%s"/>
            </label>
          </td>""" % (example.key, example.key, idx, jdx, jdx)
    html += "</tr>"
  html += """
      </table>
      </div>
      """
  return html, num_targets

def generate_2choice_instructions():
  return """
      <p>Consider the following Twitter exchange where Speaker A's Tweet is provided.</p>
      <p>Your task is to decide whose response (Speaker B or Speaker C) sounds better given what Speaker A said.</p>
      <p>If both responses are equally good, click "It's a tie."<p>
      <br/>
      <p><b>Example:</b><br/>Speaker A: can i get you something from the cafe?</p>
      <table>
        <tr><td>Speaker B: coffee would be great</td></tr>
        <tr><td>Speaker C: I don't know what to say.</td></tr>
      </table>
      <br/>
      <p>In this case, Speaker B's response is better as it directly answers Speaker A's question, so you should click the bubble next to it.</p>
      <h3>You must click the Submit button when you are finished. You must complete every question before you can click Submit.</h3>
      """

def generate_multuchoice_instructions():
  return """
      <p>Consider the following Twitter exchanges between Speakers A and B.</p>
      <p>Your task is to rank the possible responses by Speaker B from best to worst, where the best response should get the lowest ranking.</p>
      <br/>
      <p><b>Example:</b><br/>Speaker A: can i get you something from the cafe?</p>
      <table>
        <tr><td>Speaker B: coffee would be great</td></tr>
        <tr><td>Speaker B: can you believe he missed the shot?</td></tr>
        <tr><td>Speaker B: I don't know what to say.</td></tr>
      </table>
      <br/>
      <p>In this case, the first response should be given rank 1, the second rank 2, and the third rank 3.</p>
      <h3>You must click the Submit button when you are finished. You must complete every question before you can click Submit.</h3>
      """

def generate_HIT_html(num_required, tables_html, instructions):
  question_html_value = """
  <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
  <HTMLContent><![CDATA[
  <!DOCTYPE html>
  <html>
  <head>
  <link crossorigin="anonymous" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" integrity="sha384-IS73LIqjtYesmURkDE9MXKbXqYA8rvKEp/ghicjem7Vc3mGRdQRptJSz60tvrB6+" rel="stylesheet" /><!-- The following snippet enables the 'responsive' behavior on smaller screens -->
  <style>
    table {
      border-collapse: collapse;    
      display: block;
    }
    td, th {
      border: 1px solid #ccc;
    }
    th:empty {
      border: 0;
    }
    #collapseTrigger{
      color:#fff;
      display: block;
      text-decoration: none;
    }
    * {
      margin: 0; padding: 0;
    }
    tr td:nth-child(1) {
      padding-left: 10px;
      padding-right: 10px;
    }
  </style>
  <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
  <script src='https://s3.amazonaws.com/mturk-public/externalHIT_v1.js' type='text/javascript'></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script>
    $(function() {
      var col, el;
      
      $("input[type=radio]").click(function() {
         // Make sure only one radio button is enabled per column.
         el = $(this);
         col = el.data("col");
         cl = el.attr("class");

         //if cl.includes("ex-") {
         $("input." + cl + "[data-col=" + col + "]").prop("checked", false);
         //}
         el.prop("checked", true);
         console.log("Here!")

         // Only enable submit if enough radio buttons are checked.
         if ($('input:radio:checked').length >= """ + str(num_required) +  """ ) {
           $("input[type=submit]").removeAttr("disabled");  
         } else {
           $("input[type=submit]").attr("disabled", "disabled");
         }
      });
    });

    $(document).ready(function() {
        // Instructions expand/collapse
        var content = $('#instructionBody');
        var trigger = $('#collapseTrigger');
        content.show();
        $('.collapse-text').text('(Click to collapse)');
        trigger.click(function(){
            content.toggle();
            var isVisible = content.is(':visible');
            if(isVisible){
              $('.collapse-text').text('(Click to collapse)');
            }else{
              $('.collapse-text').text('(Click to expand)');
            }
        });
        // end expand/collapse
     });
  </script>
  <title>Chatbot Evaluation Task</title>
  </head>
  <body>
  <div class="col-xs-12 col-md-12"><!-- Instructions -->
    <div class="panel panel-primary">
    <!-- WARNING: the ids "collapseTrigger" and "instructionBody" are being used to enable expand/collapse feature -->
    <a class="panel-heading" href="javascript:void(0);" id="collapseTrigger"><strong>Rate Speaker B's Responses</strong> <span class="collapse-text">(Click to expand)</span> </a>
      <div class="panel-body" id="instructionBody">
      """ + instructions + """
      </div>
    </div>
  </div>
  <!-- HTML to handle creating the HIT form -->
  <form name='mturk_form' method='post' id='mturk_form' action='https://workersandbox.mturk.com/mturk/externalSubmit'>
  <input type='hidden' value='' name='assignmentId' id='assignmentId'/>
  <!-- This is where you define your question(s) --> 
  """ + tables_html + """
  <!-- HTML to handle submitting the HIT -->
  <p><input type='submit' id='submitButton' value='Submit' /></p></form>
  <h4>You must fill out rankings for every question before you can submit.</h4>
  <script language='Javascript'>turkSetAssignmentID();</script>
  </body>
  </html>
  ]]>
  </HTMLContent>
  <FrameHeight>600</FrameHeight>
  </HTMLQuestion>
  """
  return question_html_value
