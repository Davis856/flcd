package automaton

import java.io.File

class FiniteAutomaton(filename: String) {
    companion object {
        private fun stringToListOfChars(word: String) = word.map { it.toString() }
        private fun listOfCharsToString(chars: List<String>?) = chars?.joinToString("")
    }

    private lateinit var states: List<String>
    private lateinit var alphabet: List<String>
    private lateinit var initialState: String
    private lateinit var outputStates: List<String>
    private lateinit var transitions: List<Transition>

    init {
        for (line in File(filename).readLines()) {
            when (Regex("^([a-z_]*)").find(line)?.groups?.get(1)?.value) {
                "states" -> {
                    val statesWithCurlyBraces = line.substringAfter('=')
                    val states = statesWithCurlyBraces.trim().slice(1 until statesWithCurlyBraces.length - 1).trim()
                    this.states = states.split(Regex(", *"))
                }

                "alphabet" -> {
                    val alphabetWithCurlyBraces = line.substringAfter('=')
                    val alphabet =
                        alphabetWithCurlyBraces.trim().slice(1 until alphabetWithCurlyBraces.length - 1).trim()
                    this.alphabet = alphabet.split(Regex(", *"))
                }

                "out_states" -> {
                    val outStatesWithCurlyBraces = line.substringAfter('=')
                    val outStates =
                        outStatesWithCurlyBraces.trim().slice(1 until outStatesWithCurlyBraces.length - 1).trim()
                    this.outputStates = outStates.split(Regex(", *"))
                }

                "in_state" -> {
                    this.initialState = line.substringAfter('=').trim()
                }

                "transitions" -> {
                    val transitionsWithBraces = line.substringAfter('=')
                    val transitions =
                        transitionsWithBraces.trim().slice(1 until transitionsWithBraces.length - 1).trim()
                    val splitTransitions = transitions.split(Regex("; *"))
                    val computedTransitions = mutableListOf<Transition>()
                    for (transition in splitTransitions) {
                        val transitionWithoutParentheses = transition.slice(1 until transition.length - 1).trim()
                        val individualValues = transitionWithoutParentheses.split(Regex(", *"))
                        computedTransitions.add(
                            Transition(
                                individualValues[0],
                                individualValues[1],
                                individualValues[2]
                            )
                        )
                    }
                    this.transitions = computedTransitions
                }

                null -> throw Exception("Invalid line in finite automaton")
                else -> throw Exception("Invalid line in finite automaton")
            }
        }
    }

    private fun printListOfString(listName: String, list: List<String>) {
        print("$listName={")
        for ((i, state) in list.withIndex())
            if (i + 1 != list.size)
                print("$state, ")
            else print(state)
        println("}")
    }

    fun printStates() = printListOfString("states", states)
    fun printAlphabet() = printListOfString("alphabet", alphabet)
    fun printOutStates() = printListOfString("out_states", outputStates)
    fun printInState() = println("in_state=$initialState")
    fun printTransitions() {
        print("transitions={")
        for ((i, transition) in transitions.withIndex()) {
            print("(${transition.from}, ${transition.to}, ${transition.label})")
            if (i + 1 != transitions.size)
                print("; ")
        }
    }

    /**
     * Checks if the given word is accepted by the finite automaton.
     * @param word The input word as a list of letters.
     * @return True if the word is accepted, false otherwise.
     */
    fun checkAccepted(word: List<String>): Boolean {
        var state = initialState
        for (letter in word) {
            var newState: String? = null
            // Iterate through transitions to find a match
            for (transition in transitions) {
                if (transition.from == state && transition.label == letter) {
                    newState = transition.to
                    break
                }
            }
            if (newState == null) {
                // No valid transition found for the current letter
                return false
            }
            state = newState
        }
        // Check if the final state is an output state
        return state in outputStates
    }

    /**
     * Checks if the given word is accepted by the finite automaton.
     * @param word The input word as a string.
     * @return True if the word is accepted, false otherwise.
     */
    fun checkAccepted(word: String): Boolean = checkAccepted(stringToListOfChars(word))

    /**
     * Returns the longest accepted prefix of the given word.
     * @param word The input word as a list of letters.
     * @return The list representing the accepted prefix, or null if no valid prefix is found.
     */
    fun getNextAccepted(word: List<String>): List<String>? {
        var state = initialState
        val acceptedWord = mutableListOf<String>()
        for (letter in word) {
            var newState: String? = null
            // Iterate through transitions to find a match
            for (transition in transitions) {
                if (transition.from == state && transition.label == letter) {
                    newState = transition.to
                    break
                }
            }
            if (newState == null) {
                // No valid transition found for the current letter
                break
            }
            state = newState
            acceptedWord.add(letter)
        }
        // Check if the final state is an output state
        if (state !in outputStates) {
            // The final state is not an output state, return null
            return null
        }
        return acceptedWord
    }

    /**
     * Returns the longest accepted prefix of the given word.
     * @param word The input word as a string.
     * @return The string representing the accepted prefix, or null if no valid prefix is found.
     */
    fun getNextAccepted(word: String): String? = listOfCharsToString(getNextAccepted(stringToListOfChars(word)))


}