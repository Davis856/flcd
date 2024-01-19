import automaton.FiniteAutomaton
import utils.Position
import utils.PositionType

class Scanner(private val program: String, private val tokens: List<String>) {
    val symbolTable = SymbolTable()
    val pif = mutableListOf<Pair<Int, Pair<Int, Int>>>()
    private var index = 0
    private var currentLine = 1

    private fun skipWhitespace() {
        while (index < program.length && program[index].isWhitespace()) {
            if (program[index] == '\n')
                ++currentLine
            ++index
        }
    }

    private fun skipComment() {
        if (program.startsWith("//", index)) {
            while (index < program.length && program[index] != '\n')
                ++index
            return
        }
    }

    private fun treatStringConstant(): Boolean {
        val regex = Regex("^\"([a-zA-z0-9_ ]*)\"").find(program.substring(index))
        if (regex == null) {
            if (Regex("^\"[^\"]\"").containsMatchIn(program.substring(index)))
                throw ScannerException("Lexical error: Invalid characters inside string", currentLine)
            if (Regex("^\"").containsMatchIn(program.substring(index)))
                throw ScannerException("Lexical error: Unclosed quotes", currentLine)
            return false
        }
        val stringConstant = regex.groups[1]!!.value
        index += stringConstant.length + 2
        val position = symbolTable.addStringConstant(stringConstant)
        pif.add(Pair(position.positionType.code, position.pair))
        return true
    }

    private fun treatIntConstant(): Boolean {
        /*      val regex = Regex("^([+-]?[1-9][0-9]*|0)").find(program.substring(index)) ?: return false
                val intConstant = regex.groups[1]!!.value
                index += intConstant.length
                val parsedIntConstant = intConstant.toInt()
                val position = symbolTable.addIntConstant(parsedIntConstant)
                pif.add(Pair(position.positionType.code, position.pair))
                return true*/
        // Initialize a finite automaton by reading its definition from the "int_constant.in" file
        val fa = FiniteAutomaton("src/main/resources/int_constant.in")

        // Extract the next accepted prefix of the input program using the finite automaton
        val intConstant = fa.getNextAccepted(program.substring(index)) ?: return false

        // Check if the extracted intConstant starts with '+' or '-' and the previous entry in the PIF is an identifier, integer constant, or string constant
        if (intConstant[0] in listOf('+', '-') &&
            pif.size > 0 &&
            pif.last().first in listOf(PositionType.IDENTIFIER.code, PositionType.INT_CONSTANT.code, PositionType.STRING_CONSTANT.code)
        )
            return false  // Return false if the conditions are met, indicating an invalid integer constant

        // Update the index in the program string
        index += intConstant.length

        // Convert the accepted integer constant to an actual integer
        val parsedIntConstant = intConstant.toInt()

        // Add the integer constant to the symbol table and append a new entry to the PIF
        val position = symbolTable.addIntConstant(parsedIntConstant)
        pif.add(Pair(position.positionType.code, position.pair))

        return true  // Return true to indicate successful processing of an integer constant

    }

    private fun treatFromTokenList(): Boolean {
        for ((tokenIndex, token) in tokens.withIndex())
            if (program.startsWith(token, index)) {
                pif.add(Pair(tokenIndex, Position.NullPosition.pair))
                index += token.length
                return true
            }
        return false
    }

    private fun treatIdentifier(): Boolean {
        /*val regex = Regex("^([a-zA-Z_][a-zA-Z0-9_]*)").find(program.substring(index)) ?: return false
        val identifier = regex.groups[1]!!.value
        index += identifier.length
        val position = symbolTable.addIdentifier(identifier)
        pif.add(Pair(position.positionType.code, position.pair))
        return true*/
        // Initialize a finite automaton by reading its definition from the "identifier.in" file
        val fa = FiniteAutomaton("src/main/resources/identifier.in")

        // Extract the next accepted prefix of the input program using the finite automaton
        val identifier = fa.getNextAccepted(program.substring(index)) ?: return false

        // Update the index in the program string
        index += identifier.length

        // Add the identifier to the symbol table and append a new entry to the PIF
        val position = symbolTable.addIdentifier(identifier)
        pif.add(Pair(position.positionType.code, position.pair))

        return true  // Return true to indicate successful processing of an identifier

    }

    private fun nextToken() {
        skipWhitespace()
        skipComment()
        if (index == program.length)
            return
        for (function in listOf(
            Scanner::treatStringConstant,
            Scanner::treatIntConstant,
            Scanner::treatFromTokenList,
            Scanner::treatIdentifier
        ))
            if (function(this))
                return
        throw ScannerException("Lexical error: Cannot classify token", currentLine)
    }

    fun scan() {
        while (index in program.indices)
            nextToken()
    }
}