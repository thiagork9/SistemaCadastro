
;(function()
{

	typeof(require) != 'undefined' ? SyntaxHighlighter = require('shCore').SyntaxHighlighter : null;

	function Brush()
	{
		var keywords =	'break case catch continue ' +
						'default delete do else false  ' +
						'for function if in instanceof ' +
						'new null return super switch ' +
						'this throw true try typeof var while with'
						;

		var r = SyntaxHighlighter.regexLib;
		
		this.regexList = [
			{ regex: r.multiLineDoubleQuotedString,					css: 'string' },			
			{ regex: r.multiLineSingleQuotedString,					css: 'string' },			
			{ regex: r.singleLineCComments,							css: 'comments' },			
			{ regex: r.multiLineCComments,							css: 'comments' },			
			{ regex: /\s*#.*/gm,									css: 'preprocessor' },		
			{ regex: new RegExp(this.getKeywords(keywords), 'gm'),	css: 'keyword' }			
			];
	
		this.forHtmlScript(r.scriptScriptTags);
	};

	Brush.prototype	= new SyntaxHighlighter.Highlighter();
	Brush.aliases	= ['js', 'jscript', 'javascript'];

	SyntaxHighlighter.brushes.JScript = Brush;

	typeof(exports) != 'undefined' ? exports.Brush = Brush : null;
})();
