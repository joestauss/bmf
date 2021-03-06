"""Pre-made collections of films for initializing FilmRecord or FilmCollection objects."""

class GenreSet:
    """Collections of IMDB film_ids, arranged by genre. """

    class Comedy:
        tiny = { 'tt0247745'}
        # Super Troopers
        small = {'tt0074597', 'tt0105793', 'tt0362270'}
        # The Gumball Rally, Wayne's world, The Life Aquatic with Steve Zissou

    class Horror:
        large = {'tt0900357', 'tt0080516', 'tt0195714', 'tt0051418', 'tt0077745', 'tt0059297', 'tt0056606', 'tt0146336', 'tt0045888', 'tt0056943', 'tt0024188', 'tt0455760', 'tt0058620', 'tt0083722', 'tt0192731', 'tt0059096', 'tt0454841', 'tt0036341', 'tt0097368', 'tt0051622', 'tt0055505', 'tt0053459', 'tt0185371', 'tt0055304', 'tt0053925', 'tt0055018', 'tt0076162', 'tt0056725', 'tt0076786', 'tt0119345', 'tt0057449', 'tt0397065', 'tt0059821', 'tt0053219', 'tt0026663', 'tt0295700', 'tt0451957', 'tt0042376', 'tt0024368', 'tt0057608', 'tt0069995', 'tt0051744', 'tt0057128', 'tt0052602', 'tt0070917', 'tt0042544', 'tt0034587', 'tt0130018', 'tt0309593', 'tt0054988', 'tt0036104', 'tt1262416', 'tt0053363', 'tt0827782', 'tt0075005', 'tt0064747', 'tt0058333', 'tt0058403', 'tt0263488', 'tt0055830', 'tt0056993', 'tt0036027', 'tt0028478', 'tt0026685', 'tt0026912', 'tt0068503', 'tt0056552', 'tt0288477', 'tt0056368', 'tt0171363', 'tt0057379', 'tt0043456', 'tt0057129', 'tt0037635', 'tt0052207', 'tt0790686', 'tt0482606', 'tt0058700', 'tt0059646', 'tt0120627' }

    class Western:
        small = { 'tt0058461', 'tt0045591', 'tt0065134'}
        # A fistful of dollars, calamity jane, two mules for sister sara
        medium = { 'tt0058461', 'tt0045591', 'tt0065134', 'tt0066050', 'tt0064116', 'tt0056217', 'tt0060862', 'tt0040897', 'tt0076915'}
        # small +
        # a man called sledge, once upon a time in the west, the man who shot liberty vance, the professionals, the treasure of the sierra madre, the white buffalo

class ActorSet:
    """Collections of IMDB film_ids, arranged by actor.  Currently the only actor is Vincent Price."""

    class VincentPrice:
        small = {'tt0045888', 'tt0051622', 'tt0058333'}
        filmography = { "tt0099487", "tt0096875", "tt0094961", "tt0094315", "tt0091671", "tt0086981", "tt0085693", "tt0081178", "tt0079858", "tt0074260", "tt0073213", "tt0071677", "tt0071790", "tt0070791", "tt0270206", "tt0068503", "tt0066740", "tt0065597", "tt0064949", "tt0229371", "tt0064747", "tt0065125", "tt0064695", "tt0063285", "tt0061832", "tt0061451", "tt0061014", "tt0059124", "tt0059895", "tt0059821", "tt0058333", "tt0058700", "tt0056943", "tt0057608", "tt0057128", "tt0056860", "tt0056993", "tt0057449", "tt0056606", "tt0055868", "tt0056552", "tt0055864", "tt0054937", "tt0055222", "tt0055304", "tt0055152", "tt0053925", "tt0052602", "tt0053219", "tt0053363", "tt0052626", "tt0051744", "tt0051622", "tt0051016", "tt0049833", "tt0049949", "tt0049737", "tt0048642", "tt0047200", "tt0046891", "tt0045888", "tt0044825", "tt0043643", "tt0043264", "tt0041479", "tt0042325", "tt0042229", "tt0041149", "tt0041207", "tt0040876", "tt0040744", "tt0040925", "tt0037089", "tt0039581", "tt0039973", "tt0038492", "tt0038937", "tt0037865", "tt0038040", "tt0036983", "tt0037008", "tt0037465", "tt0036803", "tt0036377", "tt0032613", "tt0032281", "tt0032610", "tt0032558", "tt0032635", "tt0032049", "tt0031826", "tt0030732"}

class TestSet:
    class MixedFormat:
        tiny   = {'tt0042376', 'Tommy Boy (1995)'}
        medium = {'tt0042376', 'Tommy Boy (1995)', 'The Matrix (1984)', 'The Ice Pirates', 'beep boop im not a real movie', 'tt4'}

    one_unreleased = {'tt8820258', 'tt0859635', 'tt0247745'}
    # super troopers 1-3. the third has not been released yet (it miiiight be out sometime in 2021).
